import functools
import re
from typing import Sequence, TYPE_CHECKING

import numpy as np

import manta_lab as ml

if TYPE_CHECKING:
    from manta_lab.dtypes._interface import BatchableMedia

AVAILABLE_WINDOWS_FNAMES = re.compile('[<>:"/\?*]')


def process_max_item_exceeded(seq: Sequence["BatchableMedia"]) -> Sequence["BatchableMedia"]:
    # If media type has a max respect it
    items = seq
    if hasattr(seq[0], "MAX_ITEMS") and seq[0].MAX_ITEMS < len(seq):  # type: ignore
        print("Only %i %s will be uploaded." % (seq[0].MAX_ITEMS, seq[0].__class__.__name__))  # type: ignore
        items = seq[: seq[0].MAX_ITEMS]  # type: ignore
    return items


def free_image_ram(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        res = func(*args, **kwargs)

        # free ram
        obj = args[0]
        if obj._path:
            obj._image = None
        return res

    return wrapped_func


def numpy_to_uint8(data: np.ndarray) -> np.ndarray:
    # some images have range -1...1 or 0-1
    dmin = np.min(data)
    if dmin < 0:
        data = (data - np.min(data)) / np.ptp(data)
    if np.max(data) <= 1.0:
        data = (data * 255).astype(np.int32)

    return data.clip(0, 255).astype(np.uint8)


def guess_image_mode(data: np.ndarray) -> str:
    if data.ndim == 2:
        return "L"
    elif data.shape[-1] == 3:
        return "RGB"
    elif data.shape[-1] == 4:
        return "RGBA"
    else:
        raise ValueError()


def validate_windows_filename(filename):
    return not bool(re.search(AVAILABLE_WINDOWS_FNAMES, filename))


def matplotlib_to_plotly(matplot):
    plotly_tool = ml.util.get_module(
        "plotly.tools",
        required="plotly is required to log interactive plots, install with: pip install plotly or convert the plot to an image with `ml.Image(plt)`",
    )
    # TODO: add exceptions or assertions
    return plotly_tool.mpl_to_plotly(matplot)


def matplotlib_contains_images(matplot):
    return any(len(ax.images) > 0 for ax in matplot.axes)


def array_to_video(video: "np.ndarray") -> "np.ndarray":
    """logic is from tensorboardX"""
    np = ml.util.get_module(
        "numpy",
        required='manta_lab.Video requires numpy when passing raw data. To get it, run "pip install numpy".',
    )
    if video.ndim < 4:
        raise ValueError("Video must be atleast 4 dimensions: time, channels, height, width")
    if video.ndim == 4:
        video = video.reshape(1, *video.shape)
    b, t, c, h, w = video.shape

    if video.dtype != np.uint8:
        print("Converting video data to uint8")
        video = video.astype(np.uint8)

    def is_power2(num: int) -> bool:
        return num != 0 and ((num & (num - 1)) == 0)

    # pad to nearest power of 2, all at once
    if not is_power2(video.shape[0]):
        len_addition = int(2 ** video.shape[0].bit_length() - video.shape[0])
        video = np.concatenate((video, np.zeros(shape=(len_addition, t, c, h, w))), axis=0)

    n_rows = 2 ** ((b.bit_length() - 1) // 2)
    n_cols = video.shape[0] // n_rows

    video = np.reshape(video, newshape=(n_rows, n_cols, t, c, h, w))
    video = np.transpose(video, axes=(2, 0, 4, 1, 5, 3))
    video = np.reshape(video, newshape=(t, n_rows * h, n_cols * w, c))
    return video
