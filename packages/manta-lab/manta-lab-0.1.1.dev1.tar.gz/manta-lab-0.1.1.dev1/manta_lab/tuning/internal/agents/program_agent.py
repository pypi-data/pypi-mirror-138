import multiprocessing
import os
import platform
import queue
import signal
import subprocess
import sys
from typing import Any, Dict

from manta_lab.tuning.interface.agent import AgentError, RunStatus


# TODO: Window is differenct
# TODO: Threading is different
# TODO: MultiProcessing is different
# TODO: Subprocess is different
class ProgramProcess:
    def __init__(self, env=None, command=None, function=None, run_id=None):
        pass

    def _start(self, finished_q, env, function, run_id):
        pass

    def poll(self):
        pass

    def wait(self):
        pass

    def kill(self):
        pass

    def terminate(self):
        pass


class ProgramAgent:
    pass
