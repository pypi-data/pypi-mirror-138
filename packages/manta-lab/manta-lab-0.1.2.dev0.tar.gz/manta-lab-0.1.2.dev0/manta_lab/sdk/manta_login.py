import enum
from typing import Dict, Optional, Tuple

import click

import manta_lab as ml
from manta_lab.api import MantaAPI
from manta_lab.sdk.libs import apikey


class ApiKeyStatus(enum.Enum):
    VALID = 1
    OFFLINE = 2
    DISABLED = 3


# TODO: add silent later
class _MantaLogin:
    def __init__(self) -> None:
        self.kwargs: Optional[Dict] = None
        self._settings: Optional[ml.Settings] = None
        self._key = None
        self._relogin = None

    def setup(self, kwargs):
        self.kwargs = kwargs

        # Do not save relogin into settings as we just want to relogin once
        self._relogin = kwargs.pop("relogin", None)

        # built up login settings
        s: ml.Settings = ml.Settings()
        s.update_login(kwargs)
        ml.setup().update(settings=s)
        self._settings = ml.setup().settings

    def is_apikey_configured(self):
        return apikey.api_key(settings=self._settings) is not None

    def login(self):
        _configured = self.is_apikey_configured()
        if self._settings.relogin or self._relogin:
            _configured = False
        if not _configured:
            return False

        _connected = self.login_display()
        return _configured and _connected

    def login_display(self) -> bool:
        try:
            api = MantaAPI(self._settings)
            active_entity = api.entity
        except KeyError:
            print("Your current API Key is wrong")
            return False

        if active_entity:
            login_state_str = "Currently logged in as"
        else:
            login_state_str = "MantaLab API key is configured as"
        login_info_str = "(use `manta_lab login --relogin` to force relogin)"
        ml.termlog(
            "{} [{}] {}".format(
                login_state_str,
                click.style(active_entity, fg="yellow"),
                login_info_str,
            ),
            repeat=False,
        )

        return True

    def configure_api_key(self, key):
        if self._settings._jupyter:
            print(
                (
                    "If you're specifying your api key in code, ensure this "
                    "code is not shared publically.\nConsider setting the "
                    "MANTA_API_KEY environment variable, or running "
                    "`manta_lab login` from the command line."
                )
            )
        apikey.write_key(self._settings, key)
        self.update_session(key)
        self._key = key

    def update_session(self, key: Optional[str], status: ApiKeyStatus = ApiKeyStatus.VALID) -> None:
        settings = ml.setup().settings
        s = dict()
        if status == ApiKeyStatus.OFFLINE:
            s = dict(mode="offline")
        elif status == ApiKeyStatus.DISABLED:
            s = dict(mode="disabled")
        elif key:
            s = dict(api_key=key)
        settings.update_login(s)
        ml.setup().update(settings=settings)

        if not settings._offline:
            ml.setup().refresh_api_key()

    def _prompt_api_key(self) -> Tuple[Optional[str], ApiKeyStatus]:
        api = MantaAPI(self._settings)
        while True:
            try:
                key = apikey.prompt_api_key(
                    self._settings,
                    api=api,
                )
            except ValueError as e:
                # invalid key provided, try again
                ml.termerror(e.args[0])
                continue
            if not key:
                return None, ApiKeyStatus.OFFLINE
            return key, ApiKeyStatus.VALID

    def prompt_api_key(self):
        key, status = self._prompt_api_key()
        self.update_session(key, status=status)
        self._key = key


def _login(
    api_key=None,
    relogin=None,
    base_url=None,
):
    if ml.run is not None:
        ml.termcritical("Calling ml.login() after ml.init() has no effect.")
        return True

    kwargs = dict(locals())
    mlogin = _MantaLogin()
    mlogin.setup(kwargs)
    if mlogin._settings._offline:
        return False

    # perform a login
    logged_in = mlogin.login()

    key = kwargs.get("api_key")
    if key:
        mlogin.configure_api_key(key)

    if logged_in:
        return logged_in

    if not key:
        mlogin.prompt_api_key()

    mlogin.login_display()
    return mlogin._key or False


def login(api_key=None, relogin: bool = None, base_url: str = None):
    """
    Log in to MantaLab.

    Arguments:
        api_key: (string, optional) authentication key.
        relogin: (bool, optional) If true, will re-prompt for API key.
        base_url: (string, optional) The host to connect to.

    Returns:
        bool: if key is configured

    Raises:
        UsageError - if api_key can not configured and no tty
    """

    if ml.setup().settings._disabled:
        return True
    kwargs = dict(locals())
    configured = _login(**kwargs)
    return True if configured else False


if __name__ == "__main__":
    login()
