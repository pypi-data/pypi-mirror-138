import hashlib
import os
import shutil
import tempfile
from typing import Callable, ClassVar, Optional, TYPE_CHECKING

import manta_lab as ml
from manta_lab.dtypes import type_util

if TYPE_CHECKING:
    from manta_lab.sdk.manta_artifact import Artifact
    from manta_lab.sdk.manta_run import Run

MEDIA_TEMP_DIR = tempfile.TemporaryDirectory("manta-lab-media")


class LogUnit:
    _log_type: ClassVar[Optional[str]] = None
    _artifact: Optional["Artifact"] = None

    def __init__(self) -> None:
        self._artifact = None

    def to_json(self):
        raise NotImplementedError()

    @classmethod
    def from_json(cls, json, artifact):
        raise NotImplementedError()

    def _set_artifact(self, artifact):
        self._artifact = artifact


class Media(LogUnit):
    """
    file will be save as one of runs artifact.

    save process will be occured at bind_run

    _set_file ->
      _handle_file ->
        to_json
    """

    _log_type = "media"

    _run: Optional["Run"]
    _caption: Optional[str]
    _path: Optional[str]
    _is_tmp: Optional[bool]
    _extension: Optional[str]
    _digest: Optional[str]
    _size: Optional[int]

    def __init__(self, caption: Optional[str] = None) -> None:
        super().__init__()
        self._caption = caption

        self._run = None
        self._path = None
        self._is_tmp = None
        self._extension = None
        self._digest = None
        self._size = None

    @classmethod
    def from_json(cls, json, artifact):
        raise NotImplementedError()

    @classmethod
    def get_media_subdir(cls) -> str:
        raise NotImplementedError

    def _set_file(self, path: str, is_tmp: bool = False, extension: Optional[str] = None) -> None:
        self._path = path
        self._is_tmp = is_tmp

        if extension is None:
            _, self._extension = os.path.splitext(os.path.basename(self._path))
        else:
            if not path.endswith(extension):
                raise ValueError(
                    'Media file extension "{}" must occur at the end of path "{}".'.format(extension, path)
                )
            self._extension = extension

        with open(self._path, "rb") as f:
            self._digest = hashlib.sha256(f.read()).hexdigest()
        self._size = os.path.getsize(self._path)

    def is_bound(self) -> bool:
        return self._run is not None

    def _create_filename(self, key, step):
        return f"{key}_{step}_{self._digest[:20]}{self._extension}"

    def _handle_file(self, filename, handling_func: Callable):
        media_path = os.path.join(self.get_media_subdir(), filename)
        new_path = os.path.join(self._run.dir, media_path)

        ml.util.mkdir(os.path.dirname(new_path))
        try:
            handling_func(self._path, new_path)
        except shutil.SameFileError:
            print("Same file detected:", new_path)

        self._filename = filename
        self._path = new_path
        self._is_tmp = False

    def bind_run(self, run):
        """
        bind image to run.
        copy file to run dir and upload it.
        """

        # TODO: add more assertions
        self._run = run
        self._set_artifact(self._run.media_artifact)

    def upload_file(self, key, step, filename=None):
        """
        for optimized file upload, path can be specified.
        """
        print("upload trying...", key, filename)
        if not self.file_is_set():
            raise AssertionError("bind_to_run called before _set_file")

        if ml.env.SYS_PLATFORM == "Windows" and not type_util.validate_windows_filename(key):
            raise ValueError(f"Media {key} is invalid. Please remove invalid filename characters")

        if filename is None:
            filename = self._create_filename(key, step)
        if self._is_tmp:
            handling_func = shutil.move
        else:
            handling_func = shutil.copy

        self._handle_file(filename, handling_func)
        self._run.upload_media_on_default_artifact(self._path)

    def _get_artifact_path(self):
        assert self._run is not None
        assert self._artifact is not None
        assert self._filename is not None  # copy file called
        return f"{self._artifact._id}/{self._filename}"

    def to_json(self):
        """Serializes the object into a JSON, using a artifact to store data.

        Args:
            artifact (manta_lab.Artifact): Artifact for which this object should be generating
            JSON

        Returns:
            dict: JSON representation
        """
        json_obj = {}
        path = ml.util.to_server_slash_path(
            os.path.relpath(self._path, self._run.dir),
        )
        artifact_path = self._get_artifact_path()

        json_obj.update(
            {
                "_type": self._log_type,
                "path": path,
                "artifact_path": artifact_path,
                "digest": self._digest,
                "size": self._size,
            }
        )
        return json_obj

    def file_is_set(self) -> bool:
        return self._path is not None and self._digest is not None

    @property
    def path(self):
        return self._path

    @property
    def run(self):
        return self._run


class BatchableMedia(Media):
    def seq_to_json():
        raise NotImplementedError()
