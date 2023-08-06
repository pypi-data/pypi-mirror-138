import importlib.machinery
import logging
import multiprocessing
import os
import sys
import threading
from typing import Any, Callable, cast, Dict, Optional, TYPE_CHECKING

import manta_lab as ml

from ..interface import MessageQueueInterface
from ..internal.process import tracking_internal

if TYPE_CHECKING:
    from queue import Queue

    from manta_lab import Settings
    from manta_lab.api import MantaAPI
    from manta_lab.base.packet import Packet
    from manta_lab.sdk.manta_run import Run

logger = logging.getLogger("mant")


class BackgroundThread(threading.Thread):
    """Class to running internal process as a thread."""

    def __init__(self, target: Callable, kwargs: Dict[str, Any]) -> None:
        threading.Thread.__init__(self)

        self.name = "BackgroundThread"
        self._target = target
        self._kwargs = kwargs
        self.daemon = True
        self.pid = 0

    def run(self) -> None:
        self._target(**self._kwargs)


class BackgroundProcess:

    _api: Optional["MantaAPI"]
    _settings: Optional["Settings"]

    _done: bool
    _record_q: "Queue[Packet]"
    _result_q: "Queue[Packet]"
    _multiprocessing: multiprocessing.context.BaseContext
    tracking_pid: Optional[int]
    tracking_process: Optional[multiprocessing.process.BaseProcess]

    interface: Optional[MessageQueueInterface]

    def __init__(self, api: "MantaAPI" = None, settings: "Settings" = None) -> None:
        self._api = api
        self._settings = settings

        self._done = False
        self._record_q = None
        self._result_q = None
        self.tracking_pid = None
        self.tracking_process = None

        self.interface = None

        self._multiprocessing = multiprocessing
        self._multiprocessing_setup()

        self._save_mod_path: Optional[str] = None
        self._save_mod_spec = None

    def _multiprocessing_setup(self) -> None:
        self._settings.start_method = "thread"  # FIXME: delete this
        if self._settings.start_method == "thread":
            logger.info("multiprocessing ignored, use Threading")
            return
        else:
            # TODO: if user use multiprocessing, it will be better to use spawn only
            # https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods
            start_method = self._settings.start_method or "spawn"
            self._multiprocessing = multiprocessing.get_context(start_method)
            logger.info(f"multiprocessing start by using: {start_method}")

    def start_process(self) -> None:
        start_method = self._settings.start_method

        self.record_q = self._multiprocessing.Queue()
        self.result_q = self._multiprocessing.Queue()
        user_pid = os.getpid()

        tracking_kwargs = dict(
            api=self._api,
            settings=self._settings,
            record_q=self.record_q,
            result_q=self.result_q,
            user_pid=user_pid,
        )

        if start_method == "thread":
            self.tracking_process = BackgroundThread(
                target=tracking_internal,
                kwargs=tracking_kwargs,
            )
        else:
            self.tracking_process = self._multiprocessing.Process(
                target=tracking_internal,
                name="BackgroundProcess",
                kwargs=tracking_kwargs,
            )

        logger.info("starting background process...")
        self.tracking_process.start()
        self.tracking_pid = self.tracking_process.pid
        logger.info(f"background process is started with pid: {self.tracking_pid}")

        self.interface = MessageQueueInterface(
            api=self._api,
            process=self.tracking_process,
            record_q=self.record_q,
            result_q=self.result_q,
        )

    def hack_set_run(self, run: "Run") -> None:
        assert self.interface
        self.interface.hack_set_run(run)

    def cleanup(self):
        if self.interface:
            self.interface.join()
        if self.tracking_process:
            self.tracking_process.join()

        if self.record_q:
            self.record_q.close()
        if self.result_q:
            self.result_q.close()
