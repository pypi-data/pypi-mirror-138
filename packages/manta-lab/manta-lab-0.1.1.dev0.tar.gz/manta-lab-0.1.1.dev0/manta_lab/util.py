import argparse
import importlib
import json
import math
import os
import platform
import queue
import random
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple, Union

import manta_lab as ml
import numpy as np
import requests
import shortuuid
import yaml
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

JSON_BYTES_LIMIT = 100000


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


def to_server_slash_path(path):
    return path.replace(os.sep, "/")


def to_os_slash_path(path):
    return path.replace("/", os.sep)


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


def read_json(path):
    result = None
    with open(path, "r") as file:
        result = json.load(file)
    return result


def write_json(path, data):
    with open(path, "w") as file:
        json.dump(data, file)


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


def path_is_reference(cls, path):
    return bool(re.match(r"^(gs|s3|https?)://", path))


# dtype utils
def get_object_typename(o):
    """We determine types based on type names so we don't have to import
    (and therefore depend on) PyTorch, TensorFlow, etc.
    """
    instance_name = o.__class__.__module__ + "." + o.__class__.__name__
    if instance_name in ["builtins.module", "__builtin__.module"]:
        return o.__name__
    else:
        return instance_name


def is_tf_tensor_typename(typename):
    return typename.startswith("tensorflow.") and ("Tensor" in typename or "Variable" in typename)


def is_tf_eager_tensor_typename(typename):
    return typename.startswith("tensorflow.") and ("EagerTensor" in typename)


def is_pytorch_tensor(obj):
    import torch

    return isinstance(obj, torch.Tensor)


def is_pytorch_tensor_typename(typename):
    return typename.startswith("torch.") and ("Tensor" in typename or "Variable" in typename)


def is_jax_tensor_typename(typename):
    return typename.startswith("jaxlib.") and "DeviceArray" in typename


def get_jax_tensor(obj):
    import jax

    return jax.device_get(obj)


def is_fastai_tensor_typename(name):
    return name.startswith("fastai.") and ("Tensor" in name)


def is_pandas_data_frame_typename(name):
    return name.startswith("pandas.") and "DataFrame" in name


def is_matplotlib_typename(name):
    return name.startswith("matplotlib.")


def is_plotly_typename(name):
    return name.startswith("plotly.")


def is_plotly_figure_typename(name):
    return name.startswith("plotly.") and name.endswith(".Figure")


def is_image_typename(name):
    return name.startswith("PIL") or name


def is_numpy_array(obj):
    return np and isinstance(obj, np.ndarray)


def is_pandas_data_frame(obj):
    return is_pandas_data_frame_typename(get_object_typename(obj))


# serialize utils
def to_dict(params):
    if isinstance(params, Dict):
        return params
    elif isinstance(params, argparse.Namespace):
        return vars(params)
    elif isinstance(params, argparse.ArgumentParser):
        data = params.parse_args()
        return vars(data)
    elif isinstance(params, ml.base.Config):
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


def json_friendly(obj):
    """Convert an object into something that's more becoming of JSON"""
    converted = True
    typename = get_object_typename(obj)

    if is_tf_eager_tensor_typename(typename):
        obj = obj.numpy()
    elif is_tf_tensor_typename(typename):
        try:
            obj = obj.eval()
        except RuntimeError:
            obj = obj.numpy()
    elif is_pytorch_tensor_typename(typename) or is_fastai_tensor_typename(typename):
        try:
            if obj.requires_grad:
                obj = obj.detach()
        except AttributeError:
            pass  # before 0.4 is only present on variables

        try:
            obj = obj.data
        except RuntimeError:
            pass  # happens for Tensors before 0.4

        if obj.size():
            obj = obj.cpu().detach().numpy()
        else:
            return obj.item(), True
    elif is_jax_tensor_typename(typename):
        obj = get_jax_tensor(obj)

    if is_numpy_array(obj):
        if obj.size == 1:
            obj = obj.flatten()[0]
        elif obj.size <= 32:
            obj = obj.tolist()
    elif np and isinstance(obj, np.generic):
        obj = obj.item()
        if isinstance(obj, float) and math.isnan(obj):
            obj = None
        elif isinstance(obj, np.generic) and obj.dtype.kind == "f":
            # obj is a numpy float with precision greater than that of native python float
            # (i.e., float96 or float128). in this case obj.item() does not return a native
            # python float to avoid loss of precision, so we need to explicitly cast this
            # down to a 64bit float
            obj = float(obj)

    elif isinstance(obj, bytes):
        obj = obj.decode("utf-8")
    elif isinstance(obj, (datetime, date)):
        obj = obj.isoformat()
    elif callable(obj):
        obj = (
            "{}.{}".format(obj.__module__, obj.__qualname__)
            if hasattr(obj, "__qualname__") and hasattr(obj, "__module__")
            else str(obj)
        )
    elif isinstance(obj, float) and math.isnan(obj):
        obj = None
    else:
        converted = False
    if sys.getsizeof(obj) > JSON_BYTES_LIMIT:
        print("Serializing object of type {} that is {} bytes".format(type(obj).__name__, sys.getsizeof(obj)))
    return obj, converted


def json_friendly_val(val):
    """Make any value (including dict, slice, sequence, etc) JSON friendly"""
    if isinstance(val, dict):
        converted = {}
        for key, value in val.items:
            converted[key] = json_friendly_val(value)
        return converted
    if isinstance(val, slice):
        converted = dict(slice_start=val.start, slice_step=val.step, slice_stop=val.stop)
        return converted
    val, _ = json_friendly(val)
    if isinstance(val, Sequence) and not isinstance(val, str):
        converted = []
        for value in val:
            converted.append(json_friendly_val(value))
        return converted
    else:
        if val.__class__.__module__ not in ("builtins", "__builtin__"):
            val = str(val)
        return val


def maybe_compress_history(obj):
    # TODO: Implement
    return obj, False


def make_safe_for_json(obj):
    """Replace invalid json floats with strings. Also converts to lists and dicts."""
    if isinstance(obj, Mapping):
        return {k: make_safe_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, str):
        # str's are Sequence, so we need to short-circuit
        return obj
    elif isinstance(obj, Sequence):
        return [make_safe_for_json(v) for v in obj]
    elif isinstance(obj, float):
        if obj != obj:  # standard way to check for NaN
            return "NaN"
    return obj


def downsample(values, target_length):
    """
    TODO: Add average downsample. current algorithm just index down.
    """
    assert target_length > 1
    values = list(values)
    if len(values) < target_length:
        return values
    ratio = float(len(values) - 1) / (target_length - 1)
    result = []

    for i in range(target_length):
        result.append(values[int(i * ratio)])
    return result


# import utils
def get_module(name, required=None):
    try:
        return importlib.import_module(name)
    except Exception:
        msg = "Error importing optional module {}".format(name)
        if required:
            print(msg)
            print(required)


# generate random name
def _load_words_file(file_path):
    words = []
    with open(file_path, "r") as f:
        words = f.readlines()
        words = [w.strip() for w in words]
        words = [w for w in words if len(w) > 0 and w[0] not in [";", "#"]]
    return words


def _get_random_word(category):
    words = []
    # TODO: change using base_path. use conf file or else. changing util path will cause error here
    dir_path = os.path.join(os.path.dirname(__file__), "assets", "words", category)
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        words.extend(_load_words_file(file_path))

    return words[random.randint(0, len(words) - 1)].replace(" ", "-")


def generate_random_name():
    adj = _get_random_word("adjectives")
    noun = _get_random_word("nouns")
    # TODO: We can easily use f"{adj} {noun}"
    # if we remove every blank from the word list (eg, 'hot dog')
    return f"{adj}-{noun}"


# console
def is_unicode_safe(stream):
    """returns true if the stream supports UTF-8"""
    if not hasattr(stream, "encoding"):
        return False
    return stream.encoding in ["UTF_8", "UTF-8"]
