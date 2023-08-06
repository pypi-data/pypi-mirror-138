from argparse import Namespace
from numbers import Number
from typing import Any, Callable, Dict, Mapping, Tuple, TYPE_CHECKING, Union

from omegaconf import DictConfig, OmegaConf

if TYPE_CHECKING:
    ConfigValueType = Union[str, float, Mapping]


def load_config(data_or_path: Union[Mapping, str, Namespace]) -> Dict:
    if isinstance(data_or_path, Mapping):
        data = OmegaConf.create(data_or_path)
    elif isinstance(data_or_path, str):
        data = OmegaConf.load(data_or_path)
    elif isinstance(data_or_path, Namespace):
        data = vars(data_or_path)
    else:
        raise AttributeError("Loading config only accepts Mapping or string argument")
    return dict(data)


def ensure_tuning_config_format():
    pass


def load_tuning_config():
    pass


# TODO: (kjw) need to think depth. ex) config.param1.param2 or config.param1.param2.params3...
class Config:
    """Config

    Config object is used to save all hyperparams.
    Config can be over-written with 2 stages.
      - project config
      - user control

    Examples:
        Basic
        ```python
        ml.config.param = 0
        ```

        From ArgumentParser
        ```python
        parser = argparse.ArgumentParser()
        parser.add_argument('--something', type=int, default=123)
        args = parser.parse_args()

        ml.config.something = 0
        ml.config.update(args)
        ```

        From yaml
        ```python
        ml.config.update_yaml(yaml_path)
        ```

        Input by initiation phase
        ```python
        ml.init(config={'param1': 1, 'param2': 2})
        ```
    """

    _items: DictConfig
    _update_callback: Callable

    def __init__(self, data: Dict = None) -> None:
        object.__setattr__(self, "_items", OmegaConf.create())
        object.__setattr__(self, "_update_callback", None)

        if data:
            self.update(data)

    def _sanitize(self, k: str, v: "ConfigValueType") -> Tuple:
        k = k.strip(".|-")
        assert isinstance(v, (str, Number, Mapping))

        return k, v

    def _sanitize_dict(self, config_dict: Dict) -> Dict:
        assert isinstance(config_dict, Mapping)

        sanitized = {}
        for k, v in config_dict.items():
            if isinstance(v, (Dict, DictConfig)):
                sanitized[k] = self._sanitize_dict(v)
            else:
                k, v = self._sanitize(k, v)
                sanitized[k] = v
        return sanitized

    def update(self, data_or_path: Union[Mapping, str]):
        config_dict = load_config(data_or_path)
        config_dict = self._sanitize_dict(config_dict)
        config_omega = OmegaConf.create(config_dict)

        object.__setattr__(
            self,
            "_items",
            OmegaConf.merge(self._items, config_omega),
        )

        if self._update_callback:
            self._update_callback(self.as_dict())

    def __setitem__(self, k: str, v: "ConfigValueType"):
        self.update({k: v})

    def __setattr__(self, k: str, v: "ConfigValueType"):
        return self.__setitem__(k, v)

    def __getitem__(self, k):
        return self._items[k]

    def __getattr__(self, k):
        return self.__getitem__(k)

    def __contains__(self, k):
        return k in self._items

    def __repr__(self) -> str:
        return OmegaConf.to_yaml(self._items)

    def keys(self):
        return self.as_dict().keys()

    def values(self):
        return self.as_dict().values()

    def items(self):
        return self.as_dict().items()

    def set_callback(self, fn: Callable) -> None:
        object.__setattr__(self, "_update_callback", fn)

    def as_dict(self):
        return OmegaConf.to_container(self._items)


if __name__ == "__main__":
    t = Config({"t": {"a": 1, "b": 2, "c": {"ttt": 3}}})

    print(t)
    print("abc")
