import logging
from typing import Dict, Optional, TYPE_CHECKING

from manta_lab.base.packet import Packet, RequestPacket

from .thread import InternalManager, InternalManagerThread

if TYPE_CHECKING:
    from queue import Queue
    from threading import Event

    from manta_lab import Settings

logger = logging.getLogger(__name__)


class HandleManager(InternalManager):

    _settings: "Settings"
    _record_q: "Queue[Packet]"
    _result_q: "Queue[Packet]"
    _sender_q: "Queue[Packet]"
    _stopped: "Event"

    def __init__(
        self,
        settings: "Settings",
        record_q: "Queue[Packet]",
        result_q: "Queue[Packet]",
        sender_q: "Queue[Packet]",
        stopped: "Event",
    ) -> None:
        self._settings = settings
        self._record_q = record_q
        self._result_q = result_q
        self._sender_q = sender_q
        self._stopped = stopped

    def process(self, record: "Packet"):
        assert record.key is not None
        record_type = record.key
        if isinstance(record, RequestPacket):
            handle_func = getattr(self, f"_handle_{record_type}_request", None)
        else:
            handle_func = getattr(self, f"_handle_{record_type}", None)
        assert handle_func, f"Cant find appropriate handle function for [{record_type}]"
        handle_func(record)

    def finish(self) -> None:
        pass

    def debounce(self) -> None:
        pass

    def _dispatch_record(self, record: "Packet", always_send: bool = False) -> None:
        if not self._settings._offline or always_send:
            self._sender_q.put(record)

    def _dispatch_result(self, result: "Packet") -> None:
        self._result_q.put(result)

    def _handle_history(self, packet: "Packet"):
        self._dispatch_record(packet)

    def _handle_stats(self, packet: "Packet"):
        self._dispatch_record(packet)

    def _handle_console(self, packet: "Packet"):
        self._dispatch_record(packet)

    def _handle_meta(self, packet: "Packet"):
        self._dispatch_record(packet)

    def _handle_config(self, packet: "Packet"):
        self._dispatch_record(packet)

    def _handle_summary(self, packet: "Packet"):
        self._dispatch_record(packet)

    def _handle_artifact_request(self, packet: "Packet"):
        self._dispatch_record(packet)

    def _handle_file(self, packet: "Packet"):
        pass

    def _handle_shutdown_request(self, packet: "RequestPacket"):
        self._stopped.set()


class HandlerThread(InternalManagerThread):
    """Read records from queue and dispatch to handler routines."""

    _record_q: "Queue[Packet]"
    _result_q: "Queue[Packet]"
    _stopped: "Event"

    def __init__(
        self,
        settings: "Settings",
        record_q: "Queue[Packet]",
        result_q: "Queue[Packet]",
        stopped: "Event",
        sender_q: "Queue[Packet]",
        debounce_interval_ms: "float" = 1000,
    ) -> None:
        super(HandlerThread, self).__init__(
            input_record_q=record_q,
            result_q=result_q,
            stopped=stopped,
            debounce_interval_ms=debounce_interval_ms,
        )
        self.name = "HandlerThread"
        self._settings = settings
        self._record_q = record_q
        self._result_q = result_q
        self._stopped = stopped
        self._sender_q = sender_q

    def _setup(self) -> None:
        self._manager = HandleManager(
            settings=self._settings,
            record_q=self._record_q,
            result_q=self._result_q,
            stopped=self._stopped,
            sender_q=self._sender_q,
        )
