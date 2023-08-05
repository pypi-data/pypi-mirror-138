""" Main Manta Process

Define entries for processes,
Handling packets, request, responses
Using Threads

Threads:
    Handler: Handle packets
    Sender: packet to server

"""
import logging
import os
import sys
import threading
import time
import traceback
from datetime import datetime
from queue import Queue
from typing import List, Optional, TYPE_CHECKING

import psutil

import manta_lab as ml

from ..interface import MessageQueueInterface
from ..libs import logfile
from .handler import HandlerThread
from .sender import SenderThread

if TYPE_CHECKING:
    from manta_lab.api import MantaAPI
    from manta_lab.base.packet import Packet

    from .thread import InternalManagerThread

logger = logging.getLogger(__name__)


def tracking_internal(
    api: "MantaAPI",
    settings: "ml.Settings",
    record_q: "Queue[Packet]",
    result_q: "Queue[Packet]",
    user_pid: int = None,
) -> None:
    """Internal process function entrypoint.

    Read from record queue and dispatch work to various threads.

    Arguments:
        settings: dictionary of configuration parameters.
        record_q: records to be handled
        result_q: for sending results back

    """
    logfile.activate_logging_handler(logger, settings.log_internal_file)
    logger.info(
        "Manta tracker running at pid: {}, started at: {}".format(
            os.getpid(),
            datetime.fromtimestamp(time.time()),
        ),
    )

    stopped = threading.Event()
    threads: "List[InternalManagerThread]" = []
    terminator = _UserProcessChecker(settings=settings, user_pid=user_pid)

    send_record_q: "Queue[Packet]" = Queue()
    sender_thread = SenderThread(
        api=api,
        settings=settings,
        record_q=send_record_q,
        result_q=result_q,
        stopped=stopped,
    )
    threads.append(sender_thread)

    handler_thread = HandlerThread(
        settings=settings,
        record_q=record_q,
        result_q=result_q,
        stopped=stopped,
        sender_q=send_record_q,
    )
    threads.append(handler_thread)

    for thread in threads:
        thread.start()

    interrupt_count = 0
    while not stopped.is_set():
        try:
            while not stopped.is_set():
                time.sleep(1)
                if terminator.polling():
                    logger.error("Internal process shutdown.")
                    stopped.set()
        except KeyboardInterrupt:
            interrupt_count += 1
            logger.warning("Internal process interrupt: {}".format(interrupt_count))
        finally:
            if interrupt_count >= 2:
                logger.error("Internal process interrupted.")
                stopped.set()

    for thread in threads:
        thread.join()

    for thread in threads:
        exc_info = thread.get_exception()
        if exc_info:
            logger.error("Thread {}:".format(thread.name), exc_info=exc_info)
            print("Thread {}:".format(thread.name), file=sys.stderr)
            traceback.print_exception(*exc_info)
            ml.termerror("Internal manta error: file data was not synced")
            sys.exit(-1)


class _UserProcessChecker(object):
    """Polling user pid is alive."""

    check_process_last: Optional[float]

    def __init__(self, settings: "ml.Settings", user_pid: Optional[int]) -> None:
        self.settings = settings
        self.pid = user_pid
        self.check_process_last = None
        self.check_process_interval = settings._check_process_interval

    def polling(self) -> bool:
        if not self.check_process_interval or not self.pid:
            return False
        time_now = time.time()
        if self.check_process_last and time_now < self.check_process_last + self.check_process_interval:
            return False
        self.check_process_last = time_now

        exists = psutil.pid_exists(self.pid)
        if not exists:
            logger.warning("Internal process exiting, parent pid {} disappeared".format(self.pid))
            return True
        return False
