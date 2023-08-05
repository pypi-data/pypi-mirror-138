import base64
import binascii
import codecs
import hashlib
import os
import platform
import shutil
from typing import (
    Any,
    ByteString,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TYPE_CHECKING,
    Union,
)

import manta_lab as ml

"""
Encoding Files have 3 options, b64, hex, md5

for digesting a file, we use md5 -> b64
for create filename, we use hex
"""


def md5_hash_file(path):
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(64 * 1024), b""):
            hash_md5.update(chunk)
    return hash_md5


def file_to_md5_b64(path: str) -> str:
    """To get digest from single file"""
    return base64.b64encode(md5_hash_file(path).digest()).decode("ascii")


def file_to_md5_hex(path: str) -> str:
    return md5_hash_file(path).he0xdigest()


def b64_to_md5(b64_encoded: str):
    return base64.b64decode(b64_encoded)


def b64_to_hex(string):
    """b64 is case sensitive so that not safe for filename, convert it to hex"""
    return binascii.hexlify(base64.standard_b64decode(string)).decode("ascii")


def md5_to_hex(bytestr: ByteString):
    return codecs.getencoder("hex")(bytestr)[0].decode("ascii")


class ArtifactManifest:
    entries: Dict[str, "ArtifactFile"]

    def __init__(self, entries=None):
        self.entries = entries or {}

    def to_manifest_json(self, update_publish=False) -> Dict:
        """This is the JSON that's stored in manta_manifest.json

        If include_local is True we also include the local paths to files. This is
        used to represent an artifact that's waiting to be saved on the current
        system. We don't need to include the local paths in the artifact manifest
        contents.
        """
        entry: ArtifactFile
        contents = {}
        for entry in sorted(self.entries.values(), key=lambda k: k.path):
            if entry.is_published():
                continue

            json_entry: Dict[str, Any] = {
                "name": entry.name,
                "path": entry.path,
                "size": entry.size,
                "digest": entry.digest,
                "ref": entry.ref,
                "local_path": entry.local_path,
                "_parent_artifact_id": entry._parent_artifact_id,
            }
            contents[entry.local_path] = json_entry

            if update_publish:
                entry.mark_as_publish()

        return contents

    @classmethod
    def from_manifest_json(cls, manifest_json) -> "ArtifactManifest":
        entries: Mapping[str, ArtifactFile] = {}
        for name, val in manifest_json["contents"].items():
            entries[name] = ArtifactFile(path=name, **val)
        return cls(entries)

    def digest(self) -> str:
        hasher = hashlib.md5()
        hasher.update("manta-artifact-manifest\n".encode())
        for (name, entry) in sorted(self.entries.items(), key=lambda kv: kv[0]):
            hasher.update("{}:{}\n".format(name, entry.digest).encode())
        return hasher.hexdigest()

    def add_entry(self, entry):
        if entry.path in self.entries and entry.digest != self.entries[entry.path].digest:
            raise ValueError("Cannot add the same path twice: %s" % entry.path)
        self.entries[entry.path] = entry

    def get_entry_by_path(self, path: str) -> Optional["ArtifactFile"]:
        return self.entries.get(path)

    def get_entries_in_directory(self, directory):
        return [
            self.entries[entry_key]
            for entry_key in self.entries
            if entry_key.startswith(directory + "/")  # entries use forward slash even for windows
        ]


class ArtifactFile:
    def __init__(
        self,
        path: str,
        size: int,
        digest: str,
        version: Optional[str] = None,
        ref: Optional[str] = None,
        local_path: Optional[str] = None,
        parent_artifact_id: Optional[str] = None,
    ):
        if local_path is not None and size is None:
            raise AttributeError()

        self.name = os.path.basename(path)
        self.path = ml.util.to_server_slash_path(path)
        self.size = size
        self.digest = digest
        self.version = version
        self.ref = ref
        self.local_path = local_path
        self._parent_artifact_id = parent_artifact_id

        self._published = False

    def __repr__(self) -> str:
        if self.ref:
            summary = f"ref: {self.ref}/{self.path}"
        else:
            summary = f"digest: {self.digest}"

        return f"<ManifestEntry {summary}>"

    def is_published(self):
        return self._published

    def mark_as_publish(self):
        self._published = True

    def copy(self, cache_path, target_path):
        # file can't have colons in Windows
        if ml.env.SYS_PLATFORM == "Windows":
            # os.path.splitdrive("c:/dir") -> ("c:", "/dir")
            head, tail = os.path.splitdrive(target_path)
            target_path = head + tail.replace(":", "-")

        need_copy = not os.path.isfile(target_path) or os.stat(cache_path).st_mtime != os.stat(target_path).st_mtime
        if need_copy:
            ml.util.mkdir(os.path.dirname(target_path))
            # We use copy2, which preserves file metadata including modified
            # time (which we use above to check whether we should do the copy).
            shutil.copy2(cache_path, target_path)
        return target_path

    def download(self, root=None):
        root = root or self._parent_artifact._default_root()
        self._parent_artifact._add_download_root(root)
        manifest = self._parent_artifact._load_manifest()
        if self.entry.ref is not None:
            cache_path = manifest.storage_policy.load_reference(
                self._parent_artifact,
                self.name,
                manifest.entries[self.name],
                local=True,
            )
        else:
            cache_path = manifest.storage_policy.load_file(
                self._parent_artifact, self.name, manifest.entries[self.name]
            )

        return self.copy(cache_path, os.path.join(root, self.name))

    def ref_target(self):
        manifest = self._parent_artifact._load_manifest()
        if self.entry.ref is not None:
            return manifest.storage_policy.load_reference(
                self._parent_artifact,
                self.name,
                manifest.entries[self.name],
                local=False,
            )
        raise ValueError("Only reference entries support ref_target().")

    def ref_url(self):
        return "manta-artifact://" + b64_to_hex(self._parent_artifact.id) + "/" + self.name
