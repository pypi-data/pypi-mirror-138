import os
from typing import Any, Dict, Optional, Sequence, TYPE_CHECKING, Union

import manta_lab as ml
from manta_lab.api import MantaAPI

from . import manta_login, manta_setup
from .background.background import BackgroundProcess
from .libs import globals, logfile, version
from .manta_run import Run

if TYPE_CHECKING:
    from manta_lab.base import Settings


class _MantaInitiator:
    def __init__(self) -> None:
        self._api = None
        self.config = None
        self.settings = None
        self.observers = None
        self.logger = None

    def _setup_observers(self):  # TODO: do we really need this function?
        self.observers = []

    def _setup_configs(self, config_kwargs: Dict[str, str]):
        self.config = ml.Config()
        self.config.update(self.setter._config)
        self.config.update(config_kwargs)

    def _setup_login(self, settings):
        manta_login.login(
            api_key=settings.api_key,
            base_url=settings.base_url,
        )

    def _setup_server_settings(self, settings):
        """
        TODO:
        We think global settings from web can confuse clients
        Discuss later and decide we implement here or not
        """
        pass

    def _setup_logger(self, settings: "Settings"):
        """
        Make default dirs
        Start logging
        """
        dir_list = [
            os.path.dirname(settings.log_user_file),
            os.path.dirname(settings.log_internal_file),
            os.path.dirname(settings.latest_symlink_run_dir),
            settings.files_dir,
            settings.logs_dir,
        ]
        for d in dir_list:
            ml.util.mkdir(d)

        logfile.create_symlinks(settings)
        logfile.activate_logging_handler(self.logger, settings.log_user_file)
        self.logger.info(f"Logging user logs to {settings.log_user_file}")
        self.logger.info(f"Logging internal logs to {settings.log_internal_file}")

    def setup(self, kwargs):
        """Set Settings instance for run running

        1. Global setups
        2. Observer setups
        3. Config setups
        4. Create API, Login updates
        5. Client's Server setting updates
        6. init kwargs update
        7. Settings updates
        """
        # TODO: refactor this function
        # better inject dependencies as variable if setup functions should be called in order.
        # Assuming that function call has an implicit order as promise might lead us to misunderstanding
        # increasing possibility of making a mistake

        self.kwargs = (
            kwargs  # TODO: remove this line since self.kwargs is not defined in __init__ and is not being used anywhere
        )
        self.setter = (
            manta_setup.setup()
        )  # TODO: define property 'setter' when initializing instance to make it more clear
        self.logger = self.setter.get_logger()

        settings: "Settings" = self.setter.clone_settings()
        settings.update_times()
        settings_param = kwargs.pop(
            "settings", None
        )  # TODO: provide clue that kwargs should have key named 'settings' to override given settings
        if settings_param:
            settings.update_settings(settings_param)

        self._setup_observers()

        config_kwargs = kwargs.pop("config", None) or dict()
        self._setup_configs(config_kwargs)

        # working_dir, entity, project, run, tags, memo, save_code
        settings.update_init(
            kwargs
        )  # TODO: I think it'd be better to inject Settings as argument, rather than receiving kwargs and update settings inside the function.

        # TODO: (kjw) online / offline mode
        if not settings._offline:
            self._setup_login(settings)

        self.settings = settings
        self.setter.update(settings)

    def _set_version_messages(self, run: Run):
        messages = version.parse_version_messages(ml.__version__)
        if messages:
            if messages["upgrade_message"]:
                run.set_upgraded_version_message(messages["upgrade_message"])
            if messages["delete_message"]:
                run.set_deleted_version_message(messages["delete_message"])
            if messages["yank_message"]:
                run.set_yanked_version_message(messages["yank_message"])

    def _notify_run_created(self, settings: "Settings"):
        """
        notify run is created to server.
        get run_id from server
        update settings
        """
        if settings._offline:
            run_id = ml.util.generate_id()
        else:
            run_id = self._api.create_run(
                name=settings.run_name,
            )
            if run_id is None:
                raise ml.errors.UsageError()
        settings.update_init({"run_id": run_id})

    def init(self):
        """
        # TODO: reconsider whole process, execution order is important issue because of run_id dependencies.
        1. create api instance
        2. initiate Run, notify server
        3. start logger & version checks
        4. initiate Background process
        5. start run
        """
        settings = self.settings  # TODO: remove this line to prevent using local variable if not necessary

        # create api instance
        self._api = MantaAPI(settings=settings)
        self._api.setup()
        self._setup_server_settings(settings=settings)

        # initiate Run, notify server
        run = Run(config=self.config, settings=settings, observers=self.observers)
        self._notify_run_created(settings)

        # start logger & version checks
        self._setup_logger(settings)
        if not settings._offline:
            self._set_version_messages(run)

        # initiate Background process
        background = BackgroundProcess(api=self._api, settings=settings)
        background.start_process()
        background.hack_set_run(run)

        # start run
        run.set_background(background)
        run.on_start()
        return run


def init(
    project: Optional[str] = None,
    name: Optional[str] = None,
    artfiact_dir: Optional[str] = None,
    config: Union[Dict, str, None] = None,
    mode: Optional[str] = None,
    job_type: Optional[str] = None,
    entity: Optional[str] = None,
    id: Optional[str] = None,  # TODO: do we need resume?
    tags: Optional[Dict[str, str or int]] = None,
    memo: Optional[str] = None,
    save_code=None,  # TODO: this argument seems to be not used
    settings: Union["Settings", Dict[str, Any], None] = None,
) -> Run:
    """
    project: project name
    artfiact_dir: not yet
    config: config path
    entity: entity name, cover profile, teams both
    run: run name
    tags: tags
    memo: long description
    save_code: not yet
    """
    kwargs = dict(locals())

    initiator = _MantaInitiator()
    initiator.setup(kwargs)
    run = initiator.init()

    globals.set_globals(
        run=run,
        config=run.config,
        meta=run.meta,
        summary=run.summary,
        log=run.log,
        save=run.save,
        alarm=run.alarm,
        use_artifact=run.use_artifact,
        log_artifact=run.log_artifact,
    )

    return run


if __name__ == "__main__":
    init()
