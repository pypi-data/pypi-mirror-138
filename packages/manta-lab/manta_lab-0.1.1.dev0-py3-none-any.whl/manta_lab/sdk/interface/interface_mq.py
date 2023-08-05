import os
from typing import Any, Dict, Iterable, List, Optional, TYPE_CHECKING

import manta_lab as ml
import manta_lab.base.packet as pkt
from manta_lab.base.packet import Packet

from .interface import InterfaceBase

if TYPE_CHECKING:
    from multiprocessing.process import BaseProcess
    from queue import Queue

    from manta_lab.api import MantaAPI

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


def _wrap_request_packet(packet, resp):
    rp = pkt.RequestPacket.init_from(packet)
    rp.result = resp
    return rp


class MessageQueueInterface(InterfaceBase):
    """
    Interface connect user and tracking background.
    user logs all things through this interface.

    Interface has 2 types of contact method with Manta-Lab server.
        - publish: publish packet and dont care what happens next. use queue.
        - communicate: use async function. has version issue. need to ensure compatibilities.

    Interface can work after `hack_set_run` is called.
    That function call will be occured at `manta_lab/sdk/manta_init.py`
    """

    process: Optional["BaseProcess"]
    _process_check: bool
    record_q: Optional["Queue[Packet]"]
    result_q: Optional["Queue[Packet]"]

    def __init__(
        self,
        api: "MantaAPI" = None,
        record_q: "Queue[Packet]" = None,
        result_q: "Queue[Packet]" = None,
        process: "BaseProcess" = None,
        process_check: bool = True,
    ) -> None:
        super().__init__(api=api)

        self.record_q = record_q
        self.result_q = result_q
        self._process = process
        self._process_check = process_check

    def join(self) -> None:
        super().join()

    def _publish(self, record: "Packet", local: bool = None) -> None:
        if self._process_check and self._process and not self._process.is_alive():
            raise Exception("The tracking background process has shutdown")
        if local:
            record.control.local = local
        if self.record_q:
            self.record_q.put(record)

    """ publish functions, doesnt expect response. just let packet goes"""

    def _publish_login(self, login: pkt.LoginRequestPacket) -> None:
        # TODO: for logging
        pass

    def _publish_run(self, login: pkt.LoginRequestPacket) -> None:
        # TODO: for logging
        pass

    def _publish_history(self, history: pkt.HistoryPacket) -> None:
        packet = _wrap_packet(history)
        self._publish(packet)

    def _publish_stats(self, stats: pkt.StatsPacket) -> None:
        packet = _wrap_packet(stats)
        self._publish(packet)

    def _publish_console(self, console: pkt.ConsolePacket) -> None:
        packet = _wrap_packet(console)
        self._publish(packet)

    def _publish_summary(self, summary: pkt.SummaryPacket) -> None:
        packet = _wrap_packet(summary)
        self._publish(packet)

    def _publish_meta(self, meta: pkt.MetaPacket) -> None:
        packet = _wrap_packet(meta)
        self._publish(packet)

    def _publish_config(self, config: pkt.MetaPacket) -> None:
        packet = _wrap_packet(config)
        self._publish(packet)

    def _publish_shutdown(self) -> None:
        packet = _wrap_request_packet(pkt.ShutdownRequestPacket(), None)
        self._publish(packet)

    def _publish_artifact(self, artifact: pkt.ArtifactRequestPacket, resp=None) -> None:
        packet = _wrap_request_packet(artifact, resp)
        self._publish(packet)

    def _publish_file(self, artifact: pkt.FileUploadRequestPacket, resp=None) -> None:
        self.result_q.put(artifact)

    """ communication functions, expect response."""

    def _communicate_artifact(self, artifact: pkt.ArtifactRequestPacket) -> Dict:
        if artifact._id is None:
            resp = self._api.create_artifact(**artifact.as_dict())
            resp = resp["Id"]
        else:
            resp = artifact._id

        artifact._id = resp
        self._publish_artifact(artifact, resp)
        return resp

    def _communicate_file(self, artifact: pkt.ArtifactRequestPacket) -> Dict:
        resp = self._api.create_artifact(**artifact.as_dict())
        self._publish_artifact(artifact)
        return resp
