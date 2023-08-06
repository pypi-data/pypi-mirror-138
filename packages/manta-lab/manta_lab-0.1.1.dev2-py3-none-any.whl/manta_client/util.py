import argparse
import os
import queue
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import requests
import shortuuid
import yaml

import manta_lab as mc
from manta_lab.errors import Error

POW_10_BYTES = [
    ("B", 10 ** 0),
    ("KB", 10 ** 3),
    ("MB", 10 ** 6),
    ("GB", 10 ** 9),
    ("TB", 10 ** 12),
    ("PB", 10 ** 15),
    ("EB", 10 ** 18),
]
POW_2_BYTES = [
    ("B", 2 ** 0),
    ("KiB", 2 ** 10),
    ("MiB", 2 ** 20),
    ("GiB", 2 ** 30),
    ("TiB", 2 ** 40),
    ("PiB", 2 ** 50),
    ("EiB", 2 ** 60),
]
# directory utils
def mkdir(path: Union[str, Path], exist_ok: bool = True) -> bool:
    try:
        os.makedirs(path, exist_ok=exist_ok)
        return True
    except OSError as exc:
        print(exc)
        return False


def parent_makedirs(path: Union[str, Path], exist_ok: bool = True) -> bool:
    path = Path(path).parent
    mkdir(path)


def relative_path(path, root="."):
    root = os.path.abspath(root)
    return os.path.relpath(path, root)


# io utils
def read_yaml(path: Union[str, Path], encoding="utf-8") -> Dict:
    result = dict()

    try:
        with open(path, encoding=encoding) as f:
            for param in yaml.load_all(f, Loader=yaml.FullLoader):
                result.update(param)
    except OSError:
        print("Couldn't read yaml file: %s" % path)
    except UnicodeDecodeError:
        print("wrong encoding")
    return result


def read_config_yaml(path: Union[str, Path] = None, data: Dict = None, keyname: str = "value") -> Dict:
    if path and data is None:
        data = read_yaml(path)
    elif path is None and data:
        pass
    else:
        raise AttributeError()

    result = dict()
    for k, v in data.items():
        if isinstance(v, Dict) and keyname not in v:
            result[k] = read_config_yaml(data=v)
        else:
            result[k] = v[keyname]
    return result


def save_yaml(path: Union[str, Path], info: Dict) -> None:
    if mkdir(Path(path).parent):
        with open(path, "w") as f:
            yaml.dump(info, f)
    else:
        # TODO: (kjw) will be changed for error handling
        print("mkdir failed")


# serialize utils
def to_dict(params):
    if isinstance(params, Dict):
        return params
    elif isinstance(params, argparse.Namespace):
        return vars(params)
    elif isinstance(params, argparse.ArgumentParser):
        data = params.parse_args()
        return vars(data)
    elif isinstance(params, mc.base.Config):
        return params.as_dict()
    else:
        try:
            params = params.items()
        except Exception as e:
            print(e)
            raise AttributeError()


def json_value_sanitize(value):
    # TODO: tensor values will be change to float here
    return value


# id utils
def generate_id(length=10):
    run_gen = shortuuid.ShortUUID(alphabet=list("0123456789abcdefghijklmnopqrstuvwxyz"))
    return run_gen.random(length)


# queue utils
def read_many_from_queue(q: queue.Queue, max_items: int, timeout: int) -> List[Tuple]:
    try:
        item = q.get(True, timeout)
    except queue.Empty:
        return []
    items = [item]
    for i in range(max_items):
        try:
            item = q.get_nowait()
        except queue.Empty:
            return items
        items.append(item)
    return items


# request utils
def download_url(url, file_path):
    with requests.get(url, stream=True) as r:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    return file_path


# Python types: python, ipython, jupyter
def _get_python_type():
    try:
        from IPython import get_ipython  # type: ignore

        # Calling get_ipython can cause an ImportError
        if get_ipython() is None:
            return "python"
    except ImportError:
        return "python"
    if "terminal" in get_ipython().__module__ or "spyder" in sys.modules:
        return "ipython"
    else:
        return "jupyter"


def ensure_python():
    if _get_python_type() == "python":
        return True
    else:
        return False


def ensure_ipython():
    if _get_python_type() == "ipython":
        return True
    else:
        return False


def ensure_jupyter():
    if _get_python_type() == "jupyter":
        return True
    else:
        return False


# tune utils
def parse_tune_id(parts_dict):
    """In place parse tune path from parts dict.

    Arguments:
        parts_dict (dict): dict(entity=,project=,name=).  Modifies dict inplace.

    Returns:
        None or str if there is an error
    """

    entity = None
    project = None
    tune_id = parts_dict.get("name")
    if not isinstance(tune_id, str):
        return "Expected string tune_id"

    tune_split = tune_id.split("/")
    if len(tune_split) == 1:
        pass
    elif len(tune_split) == 2:
        split_project, tune_id = tune_split
        project = split_project or project
    elif len(tune_split) == 3:
        split_entity, split_project, tune_id = tune_split
        project = split_project or project
        entity = split_entity or entity
    else:
        return "Expected tune_id in form of tune, project/tune, or entity/project/tune"
    parts_dict.update(dict(name=tune_id, project=project, entity=entity))


# artifact utils
def to_readable_size(bytes, units=None):
    units = units or POW_10_BYTES
    unit, value = units[0]
    factor = round(float(bytes) / value, 1)
    return "{}{}".format(factor, unit) if factor < 1024 or len(units) == 1 else to_readable_size(bytes, units[1:])
