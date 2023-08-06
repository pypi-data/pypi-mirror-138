import logging
import time
from queue import Queue
from typing import Dict, Optional, TYPE_CHECKING

from manta_lab.base.packet import RequestPacket

from .pusher import FilePusher, RecordPusher
from .thread import InternalManager, InternalManagerThread

if TYPE_CHECKING:
    from threading import Event

    from manta_lab import Settings
    from manta_lab.api import MantaAPI
    from manta_lab.base.packet import Packet
    from manta_lab.sdk.manta_run import Run


logger = logging.getLogger(__name__)


class SendManager(InternalManager):

    _api: "MantaAPI"
    _settings: "Settings"
    _record_q: "Queue[Packet]"
    _result_q: "Queue[Packet]"

    _run: "Optional[Run]"
    _entity: "Optional[str]"
    _project: "Optional[str]"

    _file_pusher: "Optional[FilePusher]"
    _record_pusher: "Optional[RecordPusher]"

    def __init__(
        self,
        api: "MantaAPI",
        settings: "Settings",
        record_q: "Queue[Packet]",
        result_q: "Queue[Packet]",
    ) -> None:
        self._api = api
        self._settings = settings
        self._record_q = record_q
        self._result_q = result_q

        self._file_pusher = None
        self._record_pusher = None
        self._exit_code = 0

        self._start_pusher_threads()

    def process(self, record: "Packet") -> None:
        assert record.key is not None
        record_type = record.key
        if isinstance(record, RequestPacket):
            send_func = getattr(self, f"_send_{record_type}_request", None)
        else:
            send_func = getattr(self, f"_send_{record_type}", None)
            if record_type != "console":
                logger.debug("send: {}".format(record_type))

        assert send_func, f"Cant find appropriate send function for [{record_type}]"
        send_func(record)

    def finish(self) -> None:
        logger.info("shutting down sender")
        if self._file_pusher:
            self._file_pusher.finish()
            self._file_pusher = None
        if self._record_pusher:
            self._record_pusher.finish()
            self._record_pusher = None

    def debounce(self) -> None:
        pass

    def _start_pusher_threads(self) -> None:
        self._file_pusher = FilePusher(api=self._api)
        self._file_pusher.start()

        self._record_pusher = RecordPusher(api=self._api)
        self._record_pusher.start()

    def _send_run(self, packet: "Packet"):
        self._run = packet.run
        # TODO: self._start_pusher_threads() here or __init__?

    # FIXME: timestamp values are injected. want to change here
    def _send_history(self, packet: "Packet"):
        history = packet.history.as_dict()["item"]  # TODO: item pops
        history["_timestamp"] = time.time() * 1000
        self._record_pusher.push("histories", history)

    def _send_stats(self, packet: "Packet"):
        # self._flatten(row)
        # row["_timestamp"] = now
        # row["_runtime"] = int(now - self._run.start_time.ToSeconds())
        stats = packet.stats.as_dict()["item"]  # TODO: item pops
        stats["_timestamp"] = time.time() * 1000
        self._record_pusher.push("systems", stats)

    def _send_console(self, packet: "Packet"):
        console = packet.console.as_dict()
        console["_timestamp"] = time.time() * 1000
        self._record_pusher.push("logs", console)

    def _send_meta(self, packet: "Packet"):
        meta = packet.meta.as_dict()
        self._api.update_run_meta(meta)

    def _send_config(self, packet: "Packet"):
        config = packet.config.as_dict()
        self._api.update_run_config(config)

    def _send_summary(self, packet: "Packet"):
        summary = packet.summary.as_dict()
        self._api.update_run_summary(summary)

    def _send_artifact_request(self, packet: "Packet"):
        artifact = packet.artifact
        self._file_pusher.push(artifact)

    def _send_file(self, packet: "Packet"):
        pass


class SenderThread(InternalManagerThread):
    """Read records from queue and dispatch to sender routines."""

    _record_q: "Queue[Packet]"
    _result_q: "Queue[Packet]"
    _manager: "SendManager"

    def __init__(
        self,
        api: "MantaAPI",
        settings: "Settings",
        record_q: "Queue[Packet]",
        result_q: "Queue[Packet]",
        stopped: "Event",
        debounce_interval_ms: "float" = 30000,
    ) -> None:
        super().__init__(
            input_record_q=record_q,
            result_q=result_q,
            stopped=stopped,
            debounce_interval_ms=debounce_interval_ms,
        )
        self.name = "SenderThread"
        self._api = api
        self._settings = settings
        self._record_q = record_q
        self._result_q = result_q

    def _setup(self) -> None:
        self._manager = SendManager(
            api=self._api,
            settings=self._settings,
            record_q=self._record_q,
            result_q=self._result_q,
        )
