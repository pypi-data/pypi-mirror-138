import io
import os
from typing import Dict, Optional

import manta_lab.util as manta_util
from manta_lab.dtypes._interface import BatchableMedia, MEDIA_TEMP_DIR
from manta_lab.dtypes.type_util import array_to_video

AVAILABLE_VIDEO_EXT = ("gif", "mp4", "webm", "ogg")


class Video(BatchableMedia):
    _log_type = "video"

    # from arguments
    _caption: Optional[str]
    _fps: Optional[int]
    _format: Optional[str]
    # from __init__
    _width: Optional[int]
    _height: Optional[int]
    _channels: Optional[int]
    # from _set_file
    _path: Optional[str]
    _is_tmp: Optional[str]
    _extension: Optional[str]
    _digest: Optional[str]
    _size: Optional[str]

    def __init__(
        self,
        data_or_path,
        caption: Optional[str] = None,
        fps: int = 4,
        format: Optional[str] = None,
    ) -> None:
        super().__init__()

        self._caption = caption
        self._fps = fps
        self._format = format or "gif"

        self._width = None
        self._height = None
        self._channels = None

        if isinstance(data_or_path, str):
            self._init_from_path(data_or_path)
        elif isinstance(data_or_path, Video):
            self._init_from_manta_video(data_or_path)
        elif isinstance(data_or_path, io.BytesIO):
            self._init_from_stream(data_or_path)
        else:
            self._init_from_data(data_or_path)

    def _init_from_path(self, path):
        _, ext = os.path.splitext(path)
        ext = ext[1:].lower()
        if ext not in AVAILABLE_VIDEO_EXT:
            raise ValueError("manta_lab.Video accepts %s formats" % ", ".join(AVAILABLE_VIDEO_EXT))
        self._set_file(path, is_tmp=False)

    def _init_from_stream(self, stream):
        filename = os.path.join(MEDIA_TEMP_DIR.name, manta_util.generate_id() + "." + self._format)
        with open(filename, "wb") as f:
            f.write(stream.read())
        self._set_file(filename, is_tmp=True)

    def _init_from_data(self, data):
        """from numpy or tensors"""
        if hasattr(data, "numpy"):  # TF eager tensors
            data = data.numpy()
        elif not manta_util.is_numpy_array(data):
            raise ValueError("manta_lab.Video accepts tensor or numpy like data as input")

        mpy = manta_util.get_module(
            "moviepy.editor",
            required='manta_lab.Video requires moviepy and imageio when passing raw data.  Install with "pip install moviepy imageio"',
        )

        video_arr = array_to_video(data)
        _, self._height, self._width, self._channels = video_arr.shape

        clip = mpy.ImageSequenceClip(list(video_arr), fps=self._fps)

        temp_path = os.path.join(MEDIA_TEMP_DIR.name, manta_util.generate_id() + "." + self._format)
        kwargs = {"logger": None}
        if self._format == "gif":
            clip.write_gif(temp_path, **kwargs)
        else:
            clip.write_videofile(temp_path, **kwargs)

        self._set_file(temp_path, is_tmp=True)

    def _init_from_manta_video(self, video):
        self._caption: video._caption
        self._fps: video._fps
        self._format: video._format
        self._width: video._width
        self._height: video._height
        self._path = video._path
        self._is_tmp = video._is_tmp
        self._extension = video._extension
        self._digest = video._digest
        self._size = video._size

    @classmethod
    def from_json(cls, json_obj, artifact):
        # TODO: Implement
        return cls(
            artifact.get_path(json_obj["path"]).download(),
            caption=json_obj["caption"],
        )

    def to_json(self) -> Dict:
        json_dict = super().to_json()
        json_dict.update(
            {
                "_type": Video._log_type,
                "caption": self._caption,
                "width": self._width,
                "height": self._height,
            }
        )
        return json_dict

    def bind_run(
        self,
        run,
    ) -> None:
        super().bind_run(run)

    def upload_file(self, key, step):
        super().upload_file(key, step)

    @staticmethod
    def get_media_subdir():
        return os.path.join("media", "video")

    @staticmethod
    def seq_to_json(seq):
        # TODO: more assertions like Image
        jsons = [obj.to_json() for obj in seq]

        json_dict = {
            "_type": "videos",
            "count": len(seq),
            "contents": jsons,
            "captions": Video.all_captions(seq),
        }
        return json_dict

    @staticmethod
    def all_captions(video_list):
        captions = [a._caption for a in video_list]
        return ["" if c is None else c for c in captions]
