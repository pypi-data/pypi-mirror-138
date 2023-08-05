import atexit
import logging
import numbers
import os
import sys
import time
import traceback
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Type,
    TYPE_CHECKING,
    Union,
)

import click

import manta_lab as ml
from manta_lab import Settings
from manta_lab.api.api import MantaAPI
from manta_lab.base.packet import RunPacket, SummaryPacket

from .components import alarm  # noqa: F401
from .components import console, history, meta, stats, summary
from .libs import globals, observer, sparkline
from .manta_artifact import Artifact, LiveArtifact

if TYPE_CHECKING:
    from .background.background import BackgroundProcess

logger = logging.getLogger("manta")


class ProcessController:
    def __init__(self) -> None:
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def join(self):
        pass


EXPERIMENT_PREFIX = "run_"


class Run:
    _background: "BackgroundProcess"
    _media_artifact = Artifact
    _files_artifact = Artifact

    def __init__(
        self,
        settings: Settings = None,
        config: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
        observers: "List[observer.Observer]" = None,
    ) -> None:

        self._settings = settings
        self._config = config
        self._meta = meta

        # by set functions
        self._background = None
        self._observers = None

        # by property & setters from settings
        self._entity = None
        self._project = None
        self._id = None
        self._name = None
        self._memo = None
        self._tags = None
        self._group = None
        self._job_type = None
        self._start_time = time.time()  # TODO: history start time? settings start time?

        # for styled formatting
        self._project_url = None
        self._run_name = None
        self._run_url = None

        # initiated at on_init
        self._deleted_version_message = None
        self._yanked_version_message = None
        self._upgraded_version_message = None

        # initiated at on_start
        self.stats = None
        self.summary = None
        self.history = None
        self.console = None
        self._controller = None

        # initiated at finish
        self._exit_code = None
        self._cleanup_called = False
        self._sampled_history = []

        self.on_init(settings)

    def _setup_from_settings(self, settings):
        """TODO: Need to decide keep tracking value changes at settings instance or at run object

        if settings object is frozen, need to keep them in here
        """
        for k, v in settings.__dict__.items():
            try:
                k = k.replace(EXPERIMENT_PREFIX, "")
                setattr(self, f"_{k}", v)
            except KeyError:
                pass

    def setup_from_packet(self, pkt: RunPacket) -> None:
        self._packet = pkt
        self._entity = pkt.entity
        self._project = pkt.project
        # TODO: add config, meta, history ...

    def setup_from_packet_offline(self, pkt: RunPacket) -> None:
        self._packet = pkt

    def as_packet(self) -> RunPacket:
        pkt = RunPacket()
        # TODO: iterate run properties for copying
        pkt.run_id = self.run_id
        pkt.entity = self.entity
        pkt.project = self.project

        return pkt

    def as_dict(self) -> Dict:
        res = self.as_packet()
        res = res.as_dict()
        res["run_name"] = self.name
        return res

    def set_background(self, background):
        self._background = background

    def set_observers(self, observer):
        self._observers = observer

    # TODO: background checking decorator
    def _history_callback(self, row: dict, step: int):
        if self._background and self._background.interface:
            self._background.interface.publish_history(self, row, step)

    def _console_callback(self, name: str, data: List):
        if not data:
            return
        if self._background and self._background.interface:
            self._background.interface.publish_console(steam=name, lines=data)

    @property
    def api(self) -> MantaAPI:
        return self._background._api

    @property
    def entity(self) -> str:
        return self._entity or self.api.entity

    @property
    def project(self) -> str:
        return self._project or self.api.project

    @property
    def project_id(self) -> str:
        return self.api.project_id

    @property
    def run_id(self) -> str:
        return self.api.run_id

    @property
    def path(self) -> str:
        return "/".join([self.entity, self.project, self.run_id])

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    @property
    def meta(self) -> Dict[str, Any]:
        return self._meta

    @property
    def dir(self) -> str:
        return self._settings.files_dir

    @property
    def name(self) -> str:
        return self._settings.run_name

    @property
    def memo(self) -> str:
        return self._memo

    @memo.setter
    def memo(self, memo: str) -> None:
        self._memo = memo
        # TODO: notify to server memo is changed

    @property
    def group(self) -> str:
        return self._group

    @property
    def job_type(self) -> str:
        return self._job_type

    @property
    def tags(self) -> str:
        return self._tags

    @tags.setter
    def tags(self, tags: Sequence) -> None:
        self._tags = tuple(tags)

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def start_time(self) -> int:
        return self._start_time

    @property
    def silent(self) -> bool:
        return self._settings.silent

    @property
    def current_step(self) -> int:
        return self.history._step

    @property
    def media_artifact(self) -> Artifact:
        return self._media_artifact

    @property
    def files_artifact(self) -> Artifact:
        return self._files_artifact

    def _change_run_status(self, status):
        status = status.lower()
        assert status in ["pending", "running", "done", "error", "aborted"]
        self.api.update_run_status(status)

    def on_init(self, settings):
        self._setup_from_settings(settings)

        self._on_init_history()

    def on_start(self):
        # display run related messages
        self._on_start_display_versions()
        self._on_start_display_offline_msg()
        self._on_start_display_run_details()

        # TODO: log codes. do it on meta
        # self._save_codes()
        # TODO: show run info
        self._change_run_status("running")

        # initialize internal processors
        self._on_start_summary()
        self._on_start_controller()
        self._on_start_console()
        self._on_start_config()

        # TODO: code location can be changed
        if not self._settings._disable_stats:
            self._on_start_stats()
        if not self._settings._disable_meta:
            self._on_start_meta()
        self._on_start_artifacts()

        atexit.register(lambda: self.cleanup())

    def on_finish(self):
        """
        closing all process, threads
        """
        if self._controller:
            self._controller.stop()

        self.history.flush()
        self.stats.shutdown()
        self.summary.shutdown()
        self.console.stop()

        self._on_finish_display_exit_start()

        # if self._background and self._background.interface:
        #     self._background.interface.publish_exit(self._exit_code)

        # Wait for data to be synced
        # self._poll_exit_response = self._wait_for_finish()

        if self._background:
            self._background.cleanup()

        if self._controller:
            self._controller.join()

        self._change_run_status("done")

    def on_exit(self):
        """
        show summarized messages, url, summary, artifacts ...
        """
        self._on_exit_display_observers()
        # self._on_exit_get_sampled_history()
        self._on_exit_display_history()
        self._on_exit_display_summary()
        # self._on_exit_display_uploads()
        self._on_exit_display_exit_message()

    def _save_code(self):
        # TODO: Do this on meta save?
        pass

    # on_init methods
    def _on_init_history(self):
        self.history = history.History(self)
        self.history.set_callback(self._history_callback)

    # on_start methods
    def set_deleted_version_message(self, msg):
        self._deleted_version_message = msg

    def set_yanked_version_message(self, msg):
        self._yanked_version_message = msg

    def set_upgraded_version_message(self, msg):
        self._upgraded_version_message = msg

    def _on_start_display_versions(self) -> None:
        version_str = "Tracking run with manta-lab.v.{}".format(ml.__version__)
        ml.termlog(version_str)

        package_problem = True
        if self._deleted_version_message:
            ml.termcritical(self._deleted_version_message)
        elif self._yanked_version_message:
            ml.termwarn(self._yanked_version_message)
        else:
            package_problem = False

        if package_problem:
            if self._upgraded_version_message:
                ml.termwarn(self._upgraded_version_message)

    def _on_start_display_offline_msg(self):
        # add jupyter & more detailed messages
        if self._settings._offline and not self.silent:
            ml.termlog("MantaLab syncing is offline now")

    def _on_start_display_run_details(self):
        # TODO: add jupyter
        emojis = dict(project="", run="")
        if ml.env.SYS_PLATFORM != "Windows" and ml.util.is_unicode_safe(sys.stdout):
            emojis = dict(project="🚀", run="🏃🏻‍♀️")

        ml.termlog(f"Syncing run {self.styled_run_name}")
        ml.termlog(f"{emojis['project']} View project at {self.styled_project_url}")
        ml.termlog(f"{emojis['run']} View Run at {self.styled_run_url}")
        ml.termlog(f"Run data is saved locally in {self.styled_run_dir}")
        if not self._settings._offline:
            ml.termlog("Run `manta-lab offline` to turn off syncing.")

    def _add_style(self, msg, underline=True, fg="blue"):
        return click.style(msg, underline=underline, fg=fg)

    def _on_start_stats(self):
        self.stats = stats.SystemStats(interface=self._background.interface)
        self.stats.start()

    def _on_start_summary(self):
        self.summary = summary.Summary(interface=self._background.interface)
        self.summary.start()

    def _on_start_meta(self):
        self._meta = meta.Meta(self._settings, interface=self._background.interface)
        self._meta.collect()
        self._meta.register()

    def _on_start_config(self):
        config = ml.base.Config()
        config.update(self._config)
        self._background.interface.publish_config(config.as_dict())

    def _on_start_controller(self):
        self._controller = ProcessController()
        self._controller.start()

    def _on_start_console(self):
        # sync option = REDIRECT, WRAP, OFF
        self.console = console.ConsoleSync(self)
        self.console.set_callback(self._console_callback)
        self.console.sync(option="wrap")

    def _on_start_artifacts(self):
        self._media_artifact = LiveArtifact("media", "default")
        self.log_artifact(self._media_artifact)
        self._files_artifact = LiveArtifact("files", "default")
        self.log_artifact(self._files_artifact)

    def _on_finish_display_exit_start(self):
        if not self.silent:
            if self._background:
                pid = self._background.tracking_pid
                status_str = "Waiting for Manta process to finish, PID {}... ".format(pid)
            if not self._exit_code:
                status = "(success)."
                status_str += status
            else:
                status = "(failed {}).".format(self._exit_code)
                status_str += status
                if not self._settings._offline:
                    status_str += " Press ctrl-c to abort syncing."
            ml.termlog(status_str)

    def _on_exit_display_observers(self):
        # display observers warnings and errors
        pass

    def _on_exit_get_sampled_history(self):
        if self._background and self._background.interface:
            sampled = self.api.get_sampled_history()  # FIXME:
            # TODO: need some processings?
            self._sampled_history = sampled

    def _on_exit_display_history(self):
        # FIXME:
        if not ml.util.is_unicode_safe(sys.stdout):
            return

        max_key_len = 0
        history_rows = []
        for key in sorted(self._sampled_history):
            if key.startswith("_"):
                continue
            vals = ml.util.downsample(self._sampled_history[key], 40)
            if any((not isinstance(v, numbers.Number) for v in vals)):
                continue
            line = sparkline.sparkify(vals)
            history_rows.append((key, line))
            max_key_len = max(max_key_len, len(key))

        history_lines = ""
        format_str = "  {:>%s} {}\n" % max_key_len
        for row in history_rows:
            history_lines += format_str.format(*row)
        ml.termlog(f"Run[{self.styled_run_name}]'s history:")
        ml.termlog(f"{history_lines.rstrip()}\n")

    def _on_exit_display_summary(self):
        # FIXME:
        max_key_len = 0
        summary_rows = []
        summary = self.summary._summarize()

        for k, v in sorted(summary.items()):
            if k.startswith("_"):
                continue

            mean_v = v["mean"]
            if isinstance(mean_v, numbers.Number):
                if isinstance(mean_v, float):
                    mean_v = round(mean_v, 5)
                summary_rows.append((k, mean_v))
            else:
                continue
            max_key_len = max(max_key_len, len(k))

        summary_lines = ""
        format_str = "  {:>%s} {}\n" % max_key_len
        for row in summary_rows:
            summary_lines += format_str.format(*row)
        ml.termlog(f"Run[{self.styled_run_name}]'s summary:")
        ml.termlog(f"{summary_lines.rstrip()}\n")

    def _on_exit_display_uploads(self):
        # FIXME: add file_counts from api
        if self._settings._offline:
            return
        file_counts = self.api.count_uploaded_files()
        print("logging synced files")
        file_str = "Synced {} Manta file(s), {} media file(s), {} artifact file(s) and {} other file(s)".format(
            file_counts["manta_count"],
            file_counts["media_count"],
            file_counts["artifact_count"],
            file_counts["other_count"],
        )
        print(file_str)

    def _on_exit_display_exit_message(self):
        ml.termlog(f"Synced {self.styled_run_name}: {self.styled_run_url}")
        if self._settings._offline and not self.silent:
            ml.termlog("You can sync this run to the cloud by running:")
            ml.termlog(f"manta-lab sync {self.sytled_run_dir}")

        if not self.silent:
            ml.termlog(f"You can find logs at: {self.styled_log_dir}")

    def upload_media_on_default_artifact(self, fname: str) -> None:
        self._media_artifact.add_file(fname)
        self.log_artifact(self.media_artifact)

    def upload_file_on_default_artifact(self, fname: str) -> None:
        if not self._background or not self._background.interface:
            return
        # TODO: upload process
        # self._background.interface.publish_files(fname)

    def log(self, data: Dict[str, Any], flush: bool = True):
        """
        if key starts with `_`, then that key can be x-axis
        """
        logger.info("log called")
        if not isinstance(data, Mapping):
            raise ValueError("log inputs must be a dictionary")

        if not all(isinstance(key, str) for key in data.keys()):
            raise ValueError("Dict keys must be strings.")

        if flush:
            self.history._row_update(data)
        else:
            self.history._row_add(data)

    def use_artifact(self, artifact_or_path):
        artifact = Artifact(artifact_or_path)
        artifact.download()
        return artifact

    def log_artifact(
        self,
        artifact_or_path: Union[Artifact, str],
        name: str = None,
        group: Optional[str] = None,
        labels: Optional[List[str]] = None,
        overwrite: bool = None,
        project_level: bool = False,
        use_default: bool = False,
    ):
        """Log artifact, save files in server

        Arguments:
            artifact_or_path: (str or Artifact) A path to the contents of this artifact,
                can be in the following forms:
                    - `/local/directory`
                    - `/local/directory/file.txt`
                    - `s3://bucket/path`
                You can also pass an Artifact object created by calling
                `manta_lab.Artifact`.
            name: (str, optional) An artifact name. May be prefixed with entity/project.
                Valid names can be in the following forms:
                    - name
                    - name:version
                This will default to the basename of the pathprepended with the current
                run id  if not specified.
            group: (str) group for web view, ex) dataset, model
            labels: (list, optional) artifact tags, ex) image, audio, classification ...
            overwrite: decide manta do version controls or not.
                       if not overwrite, each artifact files names will be saved differently
            project_level:
        Returns:
            An `Artifact` object.
        """
        if isinstance(artifact_or_path, Artifact):
            artifact = artifact_or_path

            if name or group or labels:
                print("WARNING: log_artifact function doesnt change artifact properties.")
        else:
            assert name is not None
            overwrite = overwrite or False  # TODO: set by settings?
            if use_default:
                artifact = self._files_artifact
            else:
                artifact = Artifact(name=name, group=group, labels=labels, overwrite=overwrite)
            artifact.add_path(artifact_or_path)

        if not isinstance(artifact, Artifact):
            raise ValueError("You must pass an instance of manta_lab.Artifact or a " "valid file path to log_artifact")

        if not self._settings._offline:
            artifact.id = self._background.interface.communicate_artifact(artifact)
        else:
            self._background.interface.publish_artifact(artifact)
        return artifact

    def save(self):
        pass

    def alarm(self):
        pass
        alarm

    def finish(self, exit_code=None):
        self.cleanup(exit_code)
        globals.unset_globals()

    def cleanup(self, exit_code: int = None):
        if self._background is None:
            print("process exited without background configured")
            return
        if self._cleanup_called:
            return
        self._cleanup_called = True
        self._exit_code = exit_code

        try:
            self.on_finish()
        except KeyboardInterrupt:
            print("Control+C captured: Run data was not fully synced")
            if ml.util.ensure_python():
                os._exit(-1)
        except Exception as e:
            self.console.stop()
            self._background.cleanup()
            print(f"Problem occured while finishing run {e}")
            traceback.print_exception(*sys.exc_info())
            if ml.util.ensure_python():
                os._exit(-1)
        else:
            self.on_exit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Type[BaseException], *args) -> bool:
        exit_code = 0 if exc_type is None else 1
        self.finish(exit_code)

    def update_config(self, d):
        self._config.update(d)
        self._background.interface.publish_config(self._config.as_dict())

    @property
    def styled_project_url(self):
        if not self._project_url:
            self._project_url = self.api.get_project_url(self.as_dict())
        return self._add_style(self._project_url)

    @property
    def styled_run_url(self):
        if not self._run_url:
            self._run_url = self.api.get_run_url(self.as_dict())
        return self._add_style(self._run_url)

    @property
    def styled_run_name(self):
        if not self._run_name:
            self._run_name = self.api.get_run_name(self.as_dict())
        return self._add_style(self._run_name, fg="yellow")

    @property
    def styled_run_dir(self):
        return self._add_style(self._settings.run_dir, fg="yellow")

    @property
    def styled_log_dir(self):
        log_dir = self._settings.log_user_file or self._settings.log_internal_file or "."
        log_dir = log_dir.replace(os.getcwd(), ".")
        return self._add_style(log_dir, "blue")

    def log_metric(self, k, v):
        pass


def finish(exit_code: int = None) -> None:
    """
    Used when creating multiple runs in the same process.

    Arguments:
        exit_code: Set to something other than 0 to mark a run as failed
    """
    if ml.run:
        ml.run.finish(exit_code=exit_code)
