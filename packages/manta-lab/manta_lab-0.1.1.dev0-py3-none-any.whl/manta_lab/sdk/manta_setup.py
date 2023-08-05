import logging
import os
from typing import Dict, Optional, Union

import manta_lab as ml
from manta_lab import Settings
from manta_lab.util import read_config_yaml

logger = logging.getLogger("manta")


class _MantaSetupInstance:
    """Singleton instance"""

    def __init__(
        self, settings: Optional[Settings] = None, environ: Optional[Union[os._Environ, Dict[str, str]]] = None
    ) -> None:
        self._settings = None
        self._environ = environ or dict(
            os.environ
        )  # TODO: having os.environ value in a local instance property could be a security hole.
        self._config = dict()

        self._setup_settings(settings)
        self._setup_logger()
        self._setup_configs()

    @property
    def settings(self):
        return self._settings

    def _setup_settings(self, settings: Optional[Settings] = None):
        s = Settings()
        s.update_sys_configs()
        s.update_envs(
            self._environ
        )  # TODO: do we really need to keep environ variable to call s.update_envs(self._environ) after injection
        if settings:
            s.update_settings(settings)

        s.infer_settings_from_env()
        if not s.cli_only:
            s.infer_program_from_env()
        self._settings = s

    def _setup_logger(self):
        ml.termsetup(self._settings, logger)

    def _setup_configs(self):
        # update user's custom conf files except basedir or curdir configs
        # TODO: show warning, values can be overwritten
        if self._settings.config_paths:
            config_paths = self._settings.config_paths.split(",")
            for path in config_paths:
                config = read_config_yaml(path) or dict()
                self._config.update(config)

    def get_logger(self):
        return logger

    def update(self, settings: Optional[Settings] = None):  # TODO: Allowing none value for update, is it intended?
        if settings:
            s = self.clone_settings()
            s.update_settings(settings=settings)
            self._settings = s

    def clone_settings(self):
        return self._settings.duplicate()

    def refresh_api_key(self):
        # Whenever the key changes, make sure to pull in user settings
        # from server.
        pass


class _MantaGlobalSetup:
    _instance = None

    def __init__(self, settings=None):  # TODO: environ is missing in the arguments
        if _MantaGlobalSetup._instance is not None:
            _MantaGlobalSetup._instance.update(
                settings=settings
            )  # TODO: it might be dangerous to update singletone instance by simply creating a new local instance. What do you think?
        else:
            _MantaGlobalSetup._instance = _MantaSetupInstance(settings=settings)

    def __getattr__(self, name):
        return getattr(self._instance, name)

    def __setattr__(self, name):
        # TODO: do we need this ?
        # (dhk) i don't think so
        return setattr(self._instance, name)


def setup(settings=None):
    gs = _MantaGlobalSetup(settings=settings)
    return gs
