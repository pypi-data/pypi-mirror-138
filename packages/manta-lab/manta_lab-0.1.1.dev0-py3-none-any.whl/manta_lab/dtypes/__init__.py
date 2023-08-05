from typing import Optional, Sequence, Union

from manta_lab.util import (
    get_object_typename,
    is_image_typename,
    is_matplotlib_typename,
    is_pandas_data_frame,
    is_plotly_typename,
)

from . import type_util
from ._interface import BatchableMedia, LogUnit, Media
from .audio import Audio
from .graph import Edge, Graph, Node
from .html import Html
from .image import BoundingBoxes2D, Classes, Image, ImageMask, Molecule, Object3D
from .plots import Bokeh, Histogram, Matplotlib, Plotly
from .table import Table
from .video import Video

"""
All Unit/Media/BatchableMedia will be changed into json format so that server can recieve them. 

for that, each thing will be saved as artifacts. 
it will follow process below.
    - ml.log({'image': image})
    - publish_history will capture it
    - history_data_to_json called
    - save them as artifact, <project>/<run>/_files/<hash>
    - image will be duplicated. for original one and optimized one to save your traffic cost while showing them on web
    - fill artifact_manifest_id 

publish_history will use_function <history_data_to_json>
"""


def history_data_to_json(run, data: dict, step: Optional[int] = None) -> dict:
    step = step or data["_step"]

    keys = data.keys()
    for key in keys:
        val = data[key]
        if isinstance(val, dict):
            data[key] = history_data_to_json(run, val, step=step)
        else:
            data[key] = val_to_json(run, key, val, step=step)

    return data


def val_to_json(run, key, val, step):
    typename = get_object_typename(val)

    if is_pandas_data_frame(val):
        raise NotImplementedError()

    elif is_matplotlib_typename(typename) or is_plotly_typename(typename):
        val = Plotly(val)

    elif isinstance(val, Sequence) and all(isinstance(v, LogUnit) for v in val):
        assert run is not None
        if len(val) and isinstance(val[0], BatchableMedia) and all(isinstance(v, type(val[0])) for v in val):
            items = type_util.process_max_item_exceeded(val)

            for i, item in enumerate(items):
                item.bind_run(run)
                item.upload_file(key, step)

            dtype_cls = items[0]
            sequence_json = dtype_cls.seq_to_json(items)
            return sequence_json
        else:
            return [val_to_json(run, key, v, step=step) for v in val]

    if isinstance(val, LogUnit):
        if isinstance(val, Media):
            val.bind_run(run)
            val.upload_file(key, step)
        return val.to_json()

    return val


__all__ = [
    "BatchableMedia",
    "LogUnit",
    "Media",
    "Audio",
    "Edge",
    "Graph",
    "Node",
    "Html",
    "BoundingBoxes2D",
    "Classes",
    "Image",
    "ImageMask",
    "Molecule",
    "Object3D",
    "Bokeh",
    "Histogram",
    "Matplotlib",
    "Plotly",
    "Table",
    "Video",
    "history_data_to_json",
    "val_to_json",
]
