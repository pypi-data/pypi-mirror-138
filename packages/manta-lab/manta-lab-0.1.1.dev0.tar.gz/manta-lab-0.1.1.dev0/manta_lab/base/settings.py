import copy
import enum
import getpass
import itertools
import os
import platform
import socket
import sys
import tempfile
import time
from datetime import datetime
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)

import manta_lab as ml
from manta_lab.base.git_repo import GitRepo
from manta_lab.errors import Error  # noqa

settings_defaults = dict(
    base_url="https://dev.manta-lab.app",
    mode="online",
    silent=False,
    project="Undefined",
    run_name=ml.util.generate_random_name(),
    use_symlink=True,
)

ENV_PREFIX = "MANTA_"

KEY_MAPPER = {
    "id": "run_id",
    "name": "run_name",
    "tags": "run_tags",
    "memo": "run_memo",
}


def get_program() -> Optional[str]:
    program = os.getenv(ml.env.PROGRAM)
    if program:
        return program

    try:
        import __main__

        return __main__.__file__
    except (ImportError, AttributeError):
        return None


def get_program_relpath_from_gitrepo(program: str) -> Optional[str]:
    curdir = os.getcwd()
    repo = GitRepo()
    root = repo.root or curdir

    program_abs_path = os.path.join(root, os.path.relpath(curdir, root), program)
    if os.path.exists(program_abs_path):
        relative_path = os.path.relpath(program_abs_path, start=root)
        if "../" in relative_path:
            print("could not save program above cwd: %s" % program)
            return None
        return relative_path

    print("could not find program at %s" % program)
    return None


def get_manta_dir(root: str) -> str:
    root = root or "."

    if not os.access(root, os.W_OK):
        print("Path %s isn't writable, using temp directory" % root)
        path = os.path.join(tempfile.gettempdir(), "manta")
    else:
        # check hidden dir exists first
        path = os.path.join(root, ".manta")
        if not os.path.exists(path):
            path = os.path.join(root, "manta")
    return path


class Settings:
    """Setting

    Settings object is holding parameters for manta-lab flow
    Settings can be over-written with multiple phase

    after init process is done, object is frozen and registered
    as global vars

    starting with _ means it will be better user not to change its value
    """

    class UpdateSource(enum.IntEnum):
        BASE: int = 1
        ENTITY: int = 3
        PROJECT: int = 4
        USER: int = 5
        SYSTEM: int = 6
        WORKSPACE: int = 7
        ENV: int = 8
        SETUP: int = 9
        LOGIN: int = 10
        INIT: int = 11
        SETTINGS: int = 12
        ARGS: int = 13

    __frozen = False
    __source_info = dict()

    def __init__(
        self,
        base_url: str = None,
        api_key: str = None,
        mode: str = None,
        entity: str = None,
        project: str = None,
        run_id: str = None,
        run_name: str = None,
        run_memo: str = None,
        run_tags: List[str] = None,
        group: str = None,
        job_type: str = None,
        artfiact_dir: str = None,  # TODO: typo fix\
        config_paths: str = None,
        # meta related
        cuda: str = None,
        docker: str = None,
        host: str = None,
        username: str = None,
        python: str = None,
        system: str = None,
        executable: str = None,
        args: str = None,
        disable_git: bool = None,
        save_code: bool = None,
        save_requirements: bool = None,
        program: str = None,
        program_relpath: str = None,
        start_timestamp: str = None,
        # intervals, debounces
        _check_process_interval: float = 10,
        # multiprocessings
        start_method: str = None,
        # create_dirs
        log_base_spec: str = "debug.log",
        log_internal_spec: str = "debug-internal.log",
        run_dir_spec: str = "{manta_dir}/{mode}-{timestamp}-{run_id}",
        log_dir_spec: str = "{manta_dir}/{mode}-{timestamp}-{run_id}/logs",
        files_dir_spec: str = "{manta_dir}/{mode}-{timestamp}-{run_id}/files",
        temp_dir_spec: str = "{manta_dir}/{mode}-{timestamp}-{run_id}/tmp",
        # symlinks
        use_symlink: bool = None,
        latest_symlink_run_dir_spec: str = "{manta_dir}/latest-run",
        log_symlink_base_spec: str = "{manta_dir}/debug.log",
        log_symlink_internal_spec: str = "{manta_dir}/debug-internal.log",
        # cli things
        cli_only: bool = None,
        silent: bool = None,
        relogin: bool = None,
        _start_time: int = None,
        _disable_stats: bool = False,
        _disable_meta: bool = False,
        # from env
        root_dir: str = None,
        # loggings
        _show_debugs: bool = True,
        _show_info: bool = True,
        _show_warnings: bool = True,
        _show_errors: bool = True,
        _show_criticals: bool = True,
        **kwargs,
    ) -> None:
        """
        mode: online, offline, disable

        """
        kwargs = dict(locals())
        kwargs.pop("self")
        self.__dict__.update({k: None for k in kwargs})

        object.__setattr__(self, "_Settings__frozen", False)
        object.__setattr__(self, "_Settings__source_info", dict())
        self._update(kwargs, _source=self.UpdateSource.SETTINGS)
        self.update_defaults()

        self.root_dir = ml.env.get_manta_dir() or os.path.abspath(os.getcwd())

    def __copy__(self) -> "Settings":
        s = Settings()
        s.update_settings(self)
        return s

    def duplicate(self) -> "Settings":
        return copy.copy(self)

    def _priority_ok(
        self,
        k: str,
        source: Optional[int],
    ) -> bool:
        key_source: Optional[int] = self.__source_info.get(k)
        if not key_source or not source:
            return True
        if source < key_source:
            return False
        return True

    def _update(self, data: Dict[str, Any] = None, _source: Optional[int] = None, **kwargs: Any) -> None:
        if self.__frozen:
            raise TypeError("Settings object is frozen")

        data = data or dict()
        result = {}
        for check in data, kwargs:
            for k in check.keys():
                if k not in self.__dict__:
                    raise KeyError(k)
                v = check[k]
                if v is None or not self._priority_ok(k, source=_source):
                    continue
                result[k] = v

        for k, v in result.items():
            if isinstance(v, list):
                v = tuple(v)
            self.__dict__[k] = v
            if _source:
                self.__source_info[k] = _source

    def update(self, data: Dict = None, _source=None, **kwargs: Any) -> None:
        self._update(data, _source=_source, **kwargs)

    def update_defaults(self, defaults: Optional[Dict] = None) -> None:
        defaults = defaults or settings_defaults
        self._update(defaults, _source=self.UpdateSource.BASE)

    def update_envs(self, environ: os._Environ = None) -> None:
        """ """
        # TODO:(kjw) add logic for env key to usable key
        # TODO:(kjw) split tags to tuple

        environ = environ or os.environ
        data = dict()
        for k, v in environ.items():
            if k.startswith(ENV_PREFIX):
                k = k.replace(ENV_PREFIX, "").lower()
                k = KEY_MAPPER.get(k, k)
                data[k] = v
        self._update(data, _source=self.UpdateSource.ENV)

    def update_sys_configs(self) -> None:
        # TODO: (kjw) update configs from manta base dir & curdir
        pass

    def update_login(self, kwargs) -> None:
        # TODO: force only permit keys [api_key, relogin, base_url]?
        self._update(kwargs, _source=self.UpdateSource.LOGIN)

    def update_init(self, kwargs) -> None:
        converted = dict()
        for k, v in kwargs.items():
            converted[KEY_MAPPER.get(k, k)] = v
        self._update(converted, _source=self.UpdateSource.INIT)

    def update_settings(self, settings: "Settings") -> None:
        for k in settings._public_keys():
            source = settings.__source_info.get(k)
            self._update({k: settings[k]}, _source=source)

    def update_times(self) -> None:
        timestamp = int(time.time() * 1000)
        self._update({"_start_time": timestamp}, _source=self.UpdateSource.INIT)

    def keys(self) -> Iterable[str]:
        return itertools.chain(self._public_keys(), self._property_keys())

    def _public_keys(self) -> Iterator[str]:
        return filter(lambda x: not x.startswith("_Settings__"), self.__dict__)

    def _property_keys(self) -> Generator[str, None, None]:
        return (k for k, v in vars(self).items() if isinstance(v, property))

    def __getitem__(self, k: str) -> Any:
        props = self._property_keys()
        if k in props:
            return getattr(self, k)
        return self.__dict__[k]

    def __setitem__(self, k: str, v: Any) -> None:
        return self.__setattr__(k, v)

    def __setattr__(self, k: str, v: Any) -> None:
        try:
            self._update({k: v}, _source=self.UpdateSource.SETUP)
        except KeyError as e:
            raise AttributeError(str(e))
        object.__setattr__(self, k, v)

    def freeze(self):
        self.__frozen = True

    def is_frozen(self):
        return self.__frozen

    def infer_settings_from_env(self) -> None:
        s = {}
        if ml.env.SYS_PLATFORM == "Windows":
            s["use_symlink"] = False
        if self.save_code is None:
            s["save_code"] = ml.env.enable_save_code()
        if self.disable_git is None:
            s["disable_git"] = ml.env.disable_git()
        if self.host is None:
            s["host"] = socket.gethostname()
        if self.username is None:
            try:
                s["username"] = getpass.getuser()
            except KeyError:
                # KeyError in restricted environments chroot jails or docker containers.
                s["username"] = str(os.getid())

        s["args"] = sys.argv[1:]
        s["cuda"] = ml.env.get_cuda_version()
        s["executable"] = sys.executable
        s["system"] = platform.platform(aliased=True)
        s["python"] = platform.python_version()
        self.update(s, _source=self.UpdateSource.ENV)

    def infer_program_from_env(self) -> None:
        program = self.program or get_program()
        if program:
            program_relpath = self.program_relpath or get_program_relpath_from_gitrepo(program)
        else:
            program = "<No main file>"
            program_relpath = None
        s = dict(program=program, program_relpath=program_relpath)
        self.update(s, _source=self.UpdateSource.ENV)

    @property
    def _disabled(self) -> bool:
        """
        disable all functionalities include offline saving
        """
        return self.mode == "disable"

    @property
    def _offline(self) -> bool:
        """
        mode == offline will do logging process and save them at local.
        that can be synchronized later if user wants with internet connections
        """
        # be aware settings has disabled property
        return self.mode in ("disable", "offline")

    @property
    def _jupyter(self) -> bool:
        return not ml.util.ensure_python()

    @property
    def start_timestamp(self):
        try:
            timestamp = datetime.fromtimestamp(self._start_time / 1000)
            timestamp = timestamp.strftime("%Y%m%d_%H%M%S")
        except TypeError:
            timestamp = None
        return timestamp

    def _fill_path_spec(self, path):
        manta_dir = self.manta_dir or "manta"

        mode = "offline" if self._offline else "online"
        spec_dict = {
            "manta_dir": manta_dir,
            "mode": mode,
            "timestamp": self.start_timestamp,
            "run_id": self.run_id,
        }
        path = path.format(**spec_dict)
        path = os.path.expanduser(path)
        return path

    @property
    def manta_dir(self) -> str:
        return get_manta_dir(self.root_dir or "")

    @property
    def run_dir(self) -> str:
        file_path = self._fill_path_spec(self.run_dir_spec)
        return file_path

    @property
    def files_dir(self) -> str:
        file_path = self._fill_path_spec(self.files_dir_spec)
        return file_path

    @property
    def logs_dir(self) -> str:
        file_path = self._fill_path_spec(self.log_dir_spec)
        return file_path

    @property
    def log_user_file(self) -> Optional[str]:
        path = os.path.join(self.log_dir_spec, self.log_base_spec)
        return self._fill_path_spec(path)

    @property
    def log_internal_file(self) -> Optional[str]:
        path = os.path.join(self.log_dir_spec, self.log_internal_spec)
        return self._fill_path_spec(path)

    @property
    def temp_dir(self) -> str:
        return self._fill_path_spec(self.temp_dir_spec) or tempfile.gettempdir()

    @property
    def log_symlink_user_file(self) -> Optional[str]:
        return self._fill_path_spec(self.log_symlink_base_spec)

    @property
    def log_symlink_internal_file(self) -> Optional[str]:
        return self._fill_path_spec(self.log_symlink_internal_spec)

    @property
    def latest_symlink_run_dir(self) -> Optional[str]:
        return self._fill_path_spec(self.latest_symlink_run_dir_spec)


if __name__ == "__main__":
    s = Settings()
    s.update_envs()

    s.api_key
