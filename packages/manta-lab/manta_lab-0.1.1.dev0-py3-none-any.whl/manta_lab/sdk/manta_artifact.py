import functools
import multiprocessing.dummy
import os
import time
from typing import Callable, Dict, List, Optional, Sequence, Tuple, TYPE_CHECKING, Union
from urllib.parse import urlparse

import requests

import manta_lab as ml
import manta_lab.dtypes as dtypes
from manta_lab.base.packet import ArtifactManifest, ArtifactRequestPacket
from manta_lab.sdk.components.artifact import (
    ArtifactFile,
    ArtifactManifest,
    b64_to_hex,
    file_to_md5_b64,
)

if TYPE_CHECKING:
    from manta_lab import Settings
    from manta_lab.api import MantaAPI


def log_upload_time(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        ml.termlog("Upload Done. %.1fs" % (time.time() - start_time), prefix=False)
        return res

    return wrapped_func


def ensure_artifact_can_add(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        if args[0]._final:
            raise ValueError("Can't add to finalized artifact.")
        else:
            return func(*args, **kwargs)

    return wrapped_func


def ensure_file(path: str):
    if not os.path.isfile(path):
        raise ValueError(f"Path is not a file: {path}")


def ensure_directory(path: str):
    if not os.path.isdir(path):
        raise ValueError(f"Path is not a directory: {path}")


def ensure_reference(uri: str):
    url = urlparse(uri)
    if not url.scheme:
        raise ValueError("References must be URIs. To reference a local file, use file://")


def ensure_addable_obj(obj):
    obj_cls = obj.__class__
    if not issubclass(obj_cls, dtypes.LogUnit):
        addable_types = [cls.__name__ for cls in dtypes.LogUnit.__subclasses__()]
        raise ValueError(f"Found object of type {obj_cls}, expected one of {addable_types}.")


def resolve_relative_path(path: str):
    try:
        import __main__

        root = os.path.dirname(__main__.__file__)
    except (ImportError, AttributeError):
        return None

    return os.path.abspath(os.path.join(root, path))


class Artifact:

    _api: "MantaAPI"
    _id: str
    _digest: str
    _manifest: ArtifactManifest
    _added_objs: Dict
    _added_local_paths: Dict
    _incremental: bool
    _state: str  # [initiated, registered, pending, pushing, done]
    _final: bool

    def __init__(
        self,
        name: str,
        group: str,  # for group veiw at web UI
        version: Optional[str] = None,
        description: Optional[str] = None,
        use_as: Optional[str] = None,  # used or logged
        labels: Optional[str] = None,
        metadata: Optional[dict] = None,
        overwrite: Optional[bool] = None,
    ) -> None:
        self._name = name
        self._group = group
        self._version = version
        self._description = description
        self._use_as = use_as
        self._labels = labels
        self._metadata = metadata or {}
        self._overwrite = overwrite

        assert ml.api  # init assertion

        self._api = ml.api
        self._id = None
        self._digest = ""
        self._manifest = ArtifactManifest()
        self._added_objs = {}
        self._added_local_paths = {}
        self._incremental = False if overwrite else True
        self._state = "INITIATED"
        self._final = False

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, artifact_id):
        self._id = artifact_id

    @property
    def version(self) -> str:
        # do different thing if user set overwrite flag
        return self._version

    @property
    def entity(self) -> str:
        if self._id:
            return self._entity
        return self._api.settings("entity") or self._api.viewer().get("entity")  # type: ignore

    @property
    def manifest(self) -> ArtifactManifest:
        self.finalize()
        return self._manifest

    @property
    def digest(self) -> str:
        self.finalize()
        return self._digest

    @property
    def group(self) -> str:
        return self._group

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> str:
        return self._state

    @property
    def size(self) -> int:
        sizes: List[int] = []
        for entry in self._manifest.entries:
            e_size = self._manifest.entries[entry].size
            if e_size is not None:
                sizes.append(e_size)
        return sum(sizes)

    @property
    def commit_hash(self) -> str:
        if self._id:
            return self._commit_hash

        raise ValueError("Cannot access commit_hash on an artifact before it has been logged or in offline mode")

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, desc: Optional[str]) -> None:
        self._description = desc
        # TODO: update description to server

    @property
    def metadata(self) -> dict:
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: dict) -> None:
        self._metadata = metadata
        # TODO: update metadata to server

    @property
    def labels(self) -> List[str]:
        return self._labels

    @labels.setter
    def labels(self, labels: List[str]) -> None:
        self._labels = labels
        # TODO: update labels to server

    @property
    def use_as(self) -> Optional[str]:
        return self._use_as

    @property
    def incremental(self) -> bool:
        return self._incremental

    def used_by(self) -> List[str]:
        if self._id:
            return None  # TODO: self.api.artfaict_used_by()

        raise ValueError("Cannot call used_by on an artifact before it has been logged or in offline mode")

    def logged_by(self) -> str:
        if self._id:
            return None  # TODO: self.api.artifact_logged_by()

        raise ValueError("Cannot call logged_by on an artifact before it has been logged or in offline mode")

    def _add_local_file(self, rel_path: str, abs_path: str, digest: str) -> ArtifactFile:
        size = os.path.getsize(abs_path)
        rel_path = ml.util.to_server_slash_path(rel_path)

        entry = ArtifactFile(
            rel_path,
            size=size,
            digest=digest,
            local_path=abs_path,
            parent_artifact_id=self.id,
        )
        self._manifest.add_entry(entry)
        self._added_local_paths[abs_path] = entry
        return entry

    @ensure_artifact_can_add
    def add_file(
        self,
        local_path: str,
        name: Optional[str] = None,
        is_tmp: Optional[bool] = False,
    ) -> ArtifactFile:
        abs_path = resolve_relative_path(local_path)
        ensure_file(abs_path)

        rel_path = name or os.path.relpath(
            abs_path,
            start=os.path.dirname(local_path),
        )
        if rel_path == ".":
            rel_path = local_path
        digest = file_to_md5_b64(abs_path)

        if is_tmp:
            file_name = os.path.basename(rel_path)
            file_name_parts = file_name.split(".")
            file_name_parts[0] = b64_to_hex(digest)[:20]
            dir_path = os.path.dirname(rel_path)
            rel_path = os.path.join(dir_path, ".".join(file_name_parts))

        return self._add_local_file(rel_path, abs_path, digest=digest)

    @ensure_artifact_can_add
    def add_dir(self, local_path: str) -> None:
        local_path = resolve_relative_path(local_path)
        ensure_directory(local_path)

        paths = []
        for dirpath, _, filenames in os.walk(local_path, followlinks=True):
            for fname in filenames:
                abs_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(
                    abs_path,
                    start=os.path.dirname(local_path),
                )
                digest = file_to_md5_b64(abs_path)
                paths.append(
                    {
                        "rel_path": rel_path,
                        "abs_path": abs_path,
                        "digest": digest,
                    }
                )

        def add_manifest_file(file_info: Dict[str, str]) -> None:
            self._add_local_file(**file_info)

        num_threads = 8
        pool = multiprocessing.dummy.Pool(num_threads)
        pool.map(add_manifest_file, paths)
        pool.close()
        pool.join()

    @ensure_artifact_can_add
    def add_reference(
        self,
        uri: str,
        name: Optional[str] = None,
        checksum: bool = True,
        max_objects: Optional[int] = None,
    ) -> Sequence[ArtifactFile]:
        ensure_reference(uri)

        if name is not None:
            name = ml.util.to_server_slash_path(name)

        # TODO: will be implemented with s3 handler
        manifest_entries: List[ArtifactFile] = []
        for entry in manifest_entries:
            self._manifest.add_entry(entry)

        return manifest_entries

    @ensure_artifact_can_add
    def add(self, obj: dtypes.LogUnit, name: str) -> ArtifactFile:
        # TODO: need more details
        ensure_addable_obj(obj)

        obj_id = id(obj)
        if obj_id in self._added_objs:
            return self._added_objs[obj_id].entry

        name = ml.util.to_server_slash_path(name)
        entry = self._manifest.get_entry_by_path(name)
        if entry is not None:
            return entry

        entry = self.add_file(obj._path, name)
        return entry

    def finalize(self) -> None:
        """
        Marks this artifact as final, which disallows further additions to the artifact.
        This happens automatically when calling `log_artifact`.

        Returns:
            None
        """
        if self._final:
            return

        # mark final after all files are added
        self._final = True
        self._digest = self._manifest.digest()
        self._stated = "PENDING"

    def get_entry(self, name: str) -> ArtifactFile:
        if self._id:
            # TODO: implement
            pass

        raise ValueError("Cannot load paths from an artifact before it has been logged or in offline mode")

    def get(self, name: str) -> dtypes.LogUnit:
        if self._id:
            # TODO: implement
            pass

        raise ValueError("Cannot call get on an artifact before it has been logged or in offline mode")

    def _default_root(self, include_version=True):
        root = (
            os.path.join(".", "artifacts", self.name)
            if include_version
            else os.path.join(".", "artifacts", self._sequence_name)
        )

        if ml.env.SYS_PLATFORM == "Windows":
            head, tail = os.path.splitdrive(root)
            root = head + tail.replace(":", "-")
        return root

    def _download_file(self, name, root):
        return self.get_entry(name).download(root)

    def download(self, root: str = None, recursive: bool = False) -> str:
        if not self._id:
            raise ValueError("Cannot call download on an artifact before it has been logged or in offline mode")

        dirpath = root or self._default_root()
        manifest = self._manifest
        nfiles = len(manifest.entries)
        size = sum(e.size for e in manifest.entries.values()) / (1024 * 1024)  # MB
        if nfiles > 5000 or size > 50:
            ml.termlog(
                "Downloading large artifact %s, %.2fMB. %s files... " % (self._name, size, nfiles),
                newline=False,
            )

        pool = multiprocessing.dummy.Pool(32)
        pool.map(functools.partial(self._download_file, root=dirpath), manifest.entries)
        if recursive:
            pool.map(lambda artifact: artifact.download(), self._dependent_artifacts)
        pool.close()
        pool.join()

        self._is_downloaded = True

        return dirpath

    def checkout(self, root: Optional[str] = None) -> str:
        if self._id:
            return self._checkout(root=root)

        raise ValueError("Cannot call checkout on an artifact before it has been logged or in offline mode")

    def verify(self, root: Optional[str] = None) -> bool:
        if self._id:
            return self._verify(root=root)

        raise ValueError("Cannot call verify on an artifact before it has been logged or in offline mode")

    def save(
        self,
        project: Optional[str] = None,
        settings: Optional["Settings"] = None,
    ) -> None:
        if ml.run is None:
            if settings is None:
                settings = ml.Settings(silent=True)
            with ml.init(project=project, settings=settings) as run:
                run.log_artifact(self)
        else:
            ml.run.log_artifact(self)

    def delete(self) -> None:
        if self._id:
            return self._delete()

        raise ValueError("Cannot call delete on an artifact before it has been logged or in offline mode")

    def get_added_local_path_name(self, local_path: str) -> Optional[str]:
        pass

    def __setitem__(self, name: str, item: dtypes.LogUnit) -> ArtifactFile:
        return self.add(item, name)

    def __getitem__(self, name: str) -> Optional[dtypes.LogUnit]:
        return self.get(name)

    def as_packet(self, **kwargs):
        packet = ArtifactRequestPacket(
            name=self.name,
            version=self.version,
            description=self.description,
            group=self.group,
            labels=self.labels,
            metadata=self.metadata,
            _id=self.id,
            _digest=self.digest,
            _manifest=self._manifest.to_manifest_json(),
        )

        return packet


class LiveArtifact(Artifact):
    """Artifact for Media and Files artifact that doens't need any digest or versionings

    Need to care which file is sent at manifest level
    """

    @property
    def manifest(self) -> ArtifactManifest:
        self._update_manifest()
        return self._manifest

    @property
    def digest(self) -> str:
        return self._name

    def _update_manifest(self) -> None:
        pass

    def as_packet(self, **kwargs):
        packet = ArtifactRequestPacket(
            name=self.name,
            version=self.version,
            description=self.description,
            group=self.group,
            labels=self.labels,
            metadata=self.metadata,
            _id=self.id,
            _digest=self.digest,
            _manifest=self._manifest.to_manifest_json(update_publish=True),
        )

        return packet


class OldArtifact:
    def __init__(self, name, description=None, group=None, labels=None, overwrite=True) -> None:
        self.name = name
        self.description = description
        self.group = group
        self.labels = labels
        self._overwrite = overwrite

        self._id = None  # get from api
        self._settings = None
        self._manifests = {}
        self._uploaded = {}

    def setup_from_packet(self, pkt: ArtifactRequestPacket) -> None:
        self._packet = pkt
        self._entity = pkt.entity
        self._project = pkt.project
        # TODO: add config, meta, history ...

    def setup_from_packet_offline(self, pkt: ArtifactRequestPacket) -> None:
        self._packet = pkt

    def as_packet(self) -> None:
        pkt = ArtifactRequestPacket()
        # TODO: iterate run properties for copying
        for k, v in self.__dict__.items():
            # TODO: Add try/except

            if k == "_manifests":
                _v = []
                for manifest in v.values():
                    _v.append(manifest.__dict__)
            else:
                _v = v

            if k in pkt.__dict__.keys():
                pkt.__dict__[k] = _v

        # TODO: manifests should be json serialized also

        return pkt

    @property
    def id(self):
        return self._id

    def _create_manifest(self, name, size, digest, path, version, type):
        kwargs = locals()
        kwargs.pop("self")
        # TODO: do it here? or at sender phase?
        # self.api.create_artifact_file(**kwargs)
        return ArtifactManifest(**kwargs)

    def add_file(self, path, name=None, version=None, root="."):
        # TODO: root default should be '../' or '.'
        # TODO: if temporal file?
        # TODO: validate_file_can_added

        if not os.path.isfile(path):
            raise ValueError("Path is not a file: %s" % path)

        name = name or os.path.basename(path)
        size = os.path.getsize(path)
        digest = file_to_md5_b64(path)
        path = ml.util.relative_path(path, root)
        version = version
        manifest = self._create_manifest(name, size, digest, path, version, type="remote")
        self._manifests[digest] = manifest

    def add_dir(self, dir_path, version=None, root="."):
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                self.add_file(file_path)

    def add_reference(self, path):
        # Do this later
        """s3://bucket/path"""
        self.api.create_artifact_ref_manifest(path)
        # manifest = self._create_manifest(name, size, digest, path, version, type='ref')

    def add_local(self, path):
        # Do this later
        """localhost://bucket/path"""
        """https://14.94.12.123/..."""
        self.api.create_artifact_ref_manifest(path)
        # manifest = self._create_manifest(name, size, digest, path, version, type='local')

    def add_path(self, path):
        """Add path,

        directory, file

        create manifest
        """
        if os.path.isdir(path):
            return self.add_dir(path)
        elif os.path.isfile(path):
            return self.add_file(path)
        elif "://" in path:
            return self.add_reference(path)
        else:
            raise ValueError("path must be a file, directory or external reference like s3://bucket/path")

    def save(self, project=None, settings=None):
        self.sync_server()

        if ml.run is None:
            settings = settings or ml.Settings(silent=True)
            if settings.project is None and project is None:
                raise AttributeError("project must be specified")

            # TODO: user may wants artifact not belong to run
            # TODO: Do this with context management
            run = ml.init(project=project, job_type="auto", settings=settings)
            run.log_artifact(self)
        else:
            ml.run.log_artifact(self)

    def download(self):
        self.sync_server()
        # FIXME: change logic
        for artifact_id, manifests in self._uploaded:
            for manifest in manifests:
                download_url = ml.run.api.artifact_file_download_url(artifact_id, manifest["Id"])
                ml.util.download_url(download_url, manifest["relativePath"])

    def sync_server(self):
        """after uploads, update its artifact_id and manifests from serve
        #FIXME: sending too many reqs to server. need to think how to save calls
        """
        artifact = ml.run.api.get_artifact(self.id)
        for entry in artifact["manifests"]:
            self._uploaded[entry["digest"]] = entry["Id"]
            self._manifests.pop(entry["digest"], None)


class ArtifactSaver:
    _api: "MantaAPI"

    def __init__(self, api) -> None:
        self._api = api

    def save(self, artifact: "ArtifactRequestPacket", callback_fn: Optional[Callable] = None):
        upload_func = functools.partial(self._upload_file, artifact._id)

        num_threads = 8
        pool = multiprocessing.dummy.Pool(num_threads)
        pool.map(upload_func, artifact._manifest.values())
        pool.close()
        pool.join()

    def _upload_file(self, artifact_id: str, manifest: Dict):
        manifest_id = self._api.create_artifact_file(artifact_id=artifact_id, **manifest)
        url, fields = self._api.artifact_file_upload_url(artifact_id, manifest_id)

        with open(manifest["local_path"], "rb") as file:
            try:
                response = requests.post(url, files={"file": file}, data=fields)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                status_code = e.response.status_code if e.response is not None else 0
                raise e

        self._api.commit_artifact_file_uploaded(artifact_id, manifest_id)
