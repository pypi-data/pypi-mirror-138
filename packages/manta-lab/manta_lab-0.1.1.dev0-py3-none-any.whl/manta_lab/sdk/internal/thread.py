import logging
import queue
import sys
import threading
import time
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from queue import Queue
    from threading import Event

    from manta_lab.base.packet import Packet

logger = logging.getLogger(__name__)


class InternalManager:
    def process(self, record: "Packet") -> None:
        raise NotImplementedError()

    def finish(self) -> None:
        raise NotImplementedError()

    def debounce(self) -> None:
        raise NotImplementedError()


class InternalManagerThread(threading.Thread):
    """Class to manage reading from queues safely."""

    def __init__(
        self,
        input_record_q: "Queue[Packet]",
        result_q: "Queue[Packet]",
        stopped: "Event",
        debounce_interval_ms: "float" = 1000,
    ) -> None:
        threading.Thread.__init__(self)
        self._input_record_q = input_record_q
        self._result_q = result_q
        self._stopped = stopped
        self._debounce_interval_ms = debounce_interval_ms
        self._manager = None
        self._exception = None

    def _setup(self) -> None:
        raise NotImplementedError()

    def _process(self, record: "Packet") -> None:
        self._manager.process(record)

    def _finish(self) -> None:
        self._manager.finish()

    def _debounce(self) -> None:
        self._manager.debounce()

    def _run(self) -> None:
        self._setup()
        start = time.time()
        while not self._stopped.is_set():
            if time.time() - start >= self._debounce_interval_ms / 1000.0:
                self._debounce()
                start = time.time()
            try:
                record = self._input_record_q.get(timeout=1)
            except queue.Empty:
                continue
            self._process(record)

            if record.key == "shutdown":
                self._debounce()
                break

        self._finish()

    def run(self) -> None:
        try:
            self._run()
        except Exception:
            self._exception = sys.exc_info()
        finally:
            if self._exception and self._stopped:
                self._stopped.set()

    def get_exception(self) -> "Optional[Exception]":
        return self._exception


class InternalPusherThread(threading.Thread):
    pass
