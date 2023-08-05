from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union

"""

Packet: Can be saved for offline or user wants
Request & Response: interaction with server
"""


@dataclass
class _PacketDefault:
    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def update(self, source: "_PacketDefault", overwrite=False):
        _d = self.__dict__
        for k, v in source.__dict__.items():
            if k in _d:
                if overwrite or _d[k] is None:
                    _d[k] = v


@dataclass
class Packet:
    key: str
    value: Any

    # Like heartbeats
    history: Optional["HistoryPacket"] = None
    summary: Optional["SummaryPacket"] = None
    console: Optional["ConsolePacket"] = None
    stats: Optional["StatsPacket"] = None
    # Less frequent
    artifact: Optional["ArtifactPacket"] = None
    alarm: Optional["AlarmPacket"] = None
    login: Optional["LoginPacket"] = None
    run: Optional["RunPacket"] = None
    settings: Optional["SettingsPacket"] = None
    config: Optional["ConfigPacket"] = None
    meta: Optional["MetaPacket"] = None

    @classmethod
    def init_from(cls, obj):
        k = obj.__class__.__name__.lower().replace("packet", "")
        packet = cls(key=k, value=obj)
        packet.__setattr__(k, obj)
        return packet


@dataclass
class RequestPacket(Packet):
    result: Any = None
    login: Optional["LoginPacket"] = None
    run: Optional["RunPacket"] = None
    artifact: Optional["ArtifactPacket"] = None
    shutdown: Optional["ShutdownRequestPacket"] = None

    @classmethod
    def init_from(cls, obj):
        k = obj.__class__.__name__.lower().replace("requestpacket", "")
        packet = cls(key=k, value=obj)
        packet.__setattr__(k, obj)
        return packet


@dataclass
class LoginPacket(_PacketDefault):
    item: Dict[str, Union[str, int, float]] = None


@dataclass
class HistoryPacket(_PacketDefault):
    item: Dict[str, Union[str, int, float]] = None


@dataclass
class SummaryPacket(_PacketDefault):
    summary: Dict[str, Union[str, int, float]] = None


@dataclass
class ConsolePacket(_PacketDefault):
    lines: str = None
    steam: str = None  # stderr or stdout


@dataclass
class _StatsItem:
    key: str
    value: Dict


@dataclass
class StatsPacket(_PacketDefault):
    item: List[_StatsItem] = None


@dataclass
class ArtifactPacket(_PacketDefault):
    name: str = None
    version: str = None
    description: str = None
    group: str = None
    labels: List[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class ArtifactManifest:
    artifact_id: str = None
    manifest_id: str = None
    type: str = None
    name: str = None
    size: int = None
    digest: str = None
    version: int = None
    path: str = None


@dataclass
class RemoteArtifactManifest:
    artifact_id: str = None
    manifest_i1d: str = None
    type: str = None
    name: str = None
    relativePath: str = None
    size: int = None
    digest: str = None
    version: int = None


@dataclass
class ReferenceArtifactManifest:
    artifact_id: str = None
    manifest_i1d: str = None
    type: str = None
    name: str = None
    relativePath: str = None
    size: int = None
    digest: str = None
    version: int = None
    ref: str = None


@dataclass
class LocalArtifactManifest:
    artifact_id: str = None
    manifest_i1d: str = None
    type: str = None
    name: str = None
    relativePath: str = None
    size: int = None
    digest: str = None
    version: int = None
    localPath: str = None


@dataclass
class ArtifactResponse(_PacketDefault):
    run_id: str = None
    project: str = None
    entity: str = None
    type: str = None
    name: str = None
    digest: str = None
    description: str = None
    commited: str = None
    labels: List[str] = None
    manifests: List["ArtifactManifest"] = None


@dataclass
class AlarmPacket(_PacketDefault):
    title: str = None
    text: str = None
    level: str = None


@dataclass
class RunPacket(_PacketDefault):
    run_id: str = None
    entity: str = None
    project: str = None


@dataclass
class SettingsPacket(_PacketDefault):
    pass


@dataclass
class MetaPacket(_PacketDefault):
    # TODO: sync with meta dict items
    metadata: Dict = None


@dataclass
class ConfigPacket(_PacketDefault):
    config: Dict = None


@dataclass
class LoginRequestPacket(_PacketDefault):
    apikey: str = None


@dataclass
class RunRequestPacket(_PacketDefault):
    name: str = None
    project: str = None
    entity: str = None
    memo: str = None
    config: Dict = None
    metadata: Dict = None
    hyperparameter: Dict = None
    tags: Sequence = None


@dataclass
class ArtifactRequestPacket(_PacketDefault):
    name: str = None
    version: str = None
    description: str = None
    group: str = None
    labels: List[str] = None
    metadata: Dict[str, Any] = None
    _id: str = None
    _digest: str = None
    _manifest: Dict = None


@dataclass
class FileUploadRequestPacket(_PacketDefault):
    pass


@dataclass
class ShutdownRequestPacket(_PacketDefault):
    pass
