import json
import os
import time
from typing import Dict

import requests

import manta_lab as mc
import manta_lab.env as env
from manta_lab.base.settings import Settings


class _BaseClient:
    def __init__(self, settings, timeout=None, environ=None):
        self._settings = settings
        self._timeout = timeout or env.get_http_timeout()
        self._environ = environ or os.environ
        self._client = None
        self.reset_client()

    def reset_client(self):
        self._client = requests.Session()
        self._client.timeout = self._timeout
        self._client.headers.update(
            {
                "User-Agent": self.user_agent,
                "Authorization": "manta-apikey {}".format(self.api_key)
                # TODO: custom headers here
                #   ex) username, user-email
            }
        )

    @property
    def api_url(self):
        base_url = self._settings.base_url
        return f"{base_url}/api/"

    @property
    def api_key(self):
        key = mc.sdk.libs.apikey.read_manta_credential(self._settings.base_url)

        # TODO: key precedence fix
        # settings key > envkey > netrc key >
        env_key = self._environ.get(env.API_KEY)
        default_key = self._settings.api_key
        return default_key or env_key or key

    @property
    def user_agent(self):
        return "Manta-Python-SDK-v{}".format(mc.__version__)

    def get(self, endpoint, kwargs=None):
        return self._client.get(endpoint, params=kwargs)

    def post(self, endpoint, kwargs=None):
        return self._client.post(endpoint, data=kwargs)

    def delete(self, endpoint):
        return self._client.delete(endpoint)

    def request(self, request_type, endpoint, kwargs=None):
        _kwargs = dict()
        if kwargs:
            kwargs.pop("self", None)
            for k, v in kwargs.items():
                if v or isinstance(v, dict):
                    _kwargs[k] = v
        kwargs = _kwargs

        if request_type not in ["get", "post", "patch", "delete"]:
            raise AttributeError("wrong request_type")

        req_func = getattr(self._client, request_type)

        url = self.api_url + endpoint
        if request_type == "get":
            res = req_func(url, params=kwargs)
        else:
            res = req_func(url, json=kwargs)
        return res


class MantaClient:
    def __init__(
        self, settings: Settings = None, retry_timedelta: int = None, num_retries: int = 0, timeout: int = None
    ) -> None:
        """ """
        self._settings = settings or Settings()
        self.retry_timedelta = retry_timedelta
        self.num_retries = num_retries
        self.timeout = timeout

        self._client = _BaseClient(self._settings, timeout=timeout)

    @property
    def api_url(self):
        return self._client.api_url

    @property
    def api_key(self):
        return self._client.api_key

    def request(self, request_type, endpoint, params=None) -> requests.Response:
        """TODO: retrying request implementation"""
        # TODO: raise error if response is 4xx 5xx
        return self._client.request(request_type, endpoint, kwargs=params)
        while True:
            try:
                res = self._client.request(request_type, endpoint, kwargs=params)
                return res
            except Exception:
                pass

            time.sleep(1.5)
            break

    def request_json(self, request_type, endpoint, params=None) -> Dict:
        kwargs = locals()
        kwargs.pop("self")
        res = self.request(**kwargs)

        try:
            return res.json()
        except json.JSONDecodeError:
            return res.text


if __name__ == "__main__":
    c = MantaClient()
    res = c.request("get", "team/my")
    print(res)
