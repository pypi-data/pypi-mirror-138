import os
from typing import Any, Dict, Iterable, List, Optional, TYPE_CHECKING

import manta_lab as ml
import manta_lab.base.packet as pkt

if TYPE_CHECKING:
    from multiprocessing.process import BaseProcess
    from queue import Queue

    from manta_lab.api import MantaAPI
    from manta_lab.base.packet import Packet, RequestPacket

    from ..manta_artifact import Artifact
    from ..manta_run import Run

"""
Overal architectures will be changed at next version 

Interface -> Handler -> Store(Future Implement) -> Sender -> RecordStreamer

Interface: create packets, pass it to handler
Handler: handle packets, execute complex logics 
Sender: send packets or request to server 
"""


def _wrap_packet(packet):
    p = pkt.Packet.init_from(packet)
    return p


def _wrap_request_packet(packet):
    rp = pkt.RequestPacket.init_from(packet)
    return rp


class InterfaceBase(object):
    _run: Optional["Run"]
    _api: Optional["MantaAPI"]
    _drop: bool

    def __init__(self, api: "MantaAPI" = None) -> None:
        self._api = api
        self._run = None
        self._drop = False

    def set_api(self, api: "MantaAPI") -> None:
        self._api = api

    def hack_set_run(self, run: "Run") -> None:
        self._run = run

    def join(self) -> None:
        if self._drop:
            return
        _ = self._publish_shutdown()

    def _publish_shutdown(self) -> None:
        raise NotImplementedError()

    def _publish(self, record: "Packet", local: bool = None) -> None:
        raise NotImplementedError()

    """ publish functions, doesnt expect response. just let packet goes"""

    def _publish_history(self, history: pkt.HistoryPacket) -> None:
        raise NotImplementedError()

    def publish_history(self, run, data: dict, step: int):
        data = ml.dtypes.history_data_to_json(run, data, step=step)
        items = {}
        for k, v in data.items():
            items[k], _ = ml.util.json_friendly(v)

        run.summary.update(items)

        history = pkt.HistoryPacket(item=items)
        self._publish_history(history)

    def _publish_stats(self, stats: pkt.StatsPacket) -> None:
        raise NotImplementedError()

    def publish_stats(self, data: dict):
        # TODO: sync step with history
        stats = pkt.StatsPacket(item=data)
        self._publish_stats(stats)

    def _publish_console(self, console: pkt.ConsolePacket) -> None:
        raise NotImplementedError()

    def publish_console(self, steam, lines):
        console = pkt.ConsolePacket(steam=steam, lines=lines)
        self._publish_console(console)

    def _publish_summary(self, summary: pkt.SummaryPacket) -> None:
        raise NotImplementedError()

    def publish_summary(self, data: dict):
        summary = pkt.SummaryPacket(summary=data)
        self._publish_summary(summary)

    def _publish_meta(self, meta: pkt.MetaPacket) -> None:
        raise NotImplementedError()

    def publish_meta(self, data: dict):
        meta = pkt.MetaPacket(metadata=data)
        self._publish_meta(meta)

    def _publish_config(self, config: pkt.MetaPacket) -> None:
        raise NotImplementedError()

    def publish_config(self, data: dict):
        config = pkt.ConfigPacket(config=data)
        self._publish_config(config)

    def _publish_artifact(self, artifact: pkt.ArtifactRequestPacket) -> str:
        raise NotImplementedError()

    def publish_artifact(self, artifact: "Artifact") -> str:
        packet = artifact.as_packet()
        resp = self._publish_artifact(packet)
        return resp

    """ communication functions, expect response."""

    def _communicate_artifact(self, artifact: pkt.ArtifactRequestPacket) -> str:
        raise NotImplementedError()

    def communicate_artifact(self, artifact: "Artifact") -> str:
        packet = artifact.as_packet()
        resp = self._communicate_artifact(packet)
        return resp
