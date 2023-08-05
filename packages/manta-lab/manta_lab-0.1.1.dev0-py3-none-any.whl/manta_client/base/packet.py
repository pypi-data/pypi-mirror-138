import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

"""

Packet: Can be saved for offline or user wants
Request & Response: interaction with server
"""


@dataclass
class _PacketDefault:
    _timestamp: int = None

    def as_dict(self):
        return self.__dict__

    def update(self, source: "_PacketDefault", overwrite=False):
        _d = self.__dict__
        for k, v in source.__dict__.items():
            if k in _d:
                if overwrite or _d[k] is None:
                    _d[k] = v

    def __post_init__(self):
        self._timestamp = int(time.time() * 1000)


@dataclass
class Packet:
    key: str
    value: Any
    req_result: int = 0  # 0 for false, 1 for true
    result: Optional["Response"] = None

    # Like heartbeats
    history: Optional["HistoryPacket"] = None
    summary: Optional["SummaryPacket"] = None
    console: Optional["ConsolePacket"] = None
    stats: Optional["StatsPacket"] = None
    # Less frequent
    artifact: Optional["ArtifactPacket"] = None
    alarm: Optional["AlarmPacket"] = None
    experiment: Optional["ExperimentPacket"] = None
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
class HistoryPacket(_PacketDefault):
    item: Dict[str, Union[str, int, float]] = None


@dataclass
class SummaryPacket(_PacketDefault):
    summary: Dict[str, Union[str, int, float]] = None


@dataclass
class ConsolePacket(_PacketDefault):
    lines: str = None
    _stream: str = None  # stderr or stdout


@dataclass
class _StatsItem:
    key: str
    value: Dict


@dataclass
class StatsPacket(_PacketDefault):
    item: List[_StatsItem] = None
    _step: int = None


@dataclass
class ArtifactPacket(_PacketDefault):
    experiment_id: Optional[str] = None
    project_id: str = None
    name: str = None
    description: str = None
    group: str = None
    labels: List[str] = None
    metadata: Dict[str, Any] = None
    _manifests: List[Dict[str, Any]] = None


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
    experiment_id: str = None
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
class ExperimentPacket(_PacketDefault):
    experiment_id: str = None
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
class Request:
    pass


@dataclass
class Response:
    pass


@dataclass
class LoginRequest:
    pass


@dataclass
class LoginResponse:
    pass


@dataclass
class ExperimentStartRequest:
    pass


@dataclass
class ExperimentStartResponse:
    pass


@dataclass
class ArtifactRequest:
    pass
