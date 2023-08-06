import ctypes
import enum
import os
import queue
import socket
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict

import manta_lab as ml

# TODO: make more abstract agent, remove tune_id for generalized agents


def parse_tune_id(parts_dict):
    """In place parse tune path from parts dict.

    Arguments:
        parts_dict (dict): dict(entity=,project=,name=).  Modifies dict inplace.

    Returns:
        None or str if there is an error
    """

    entity = None
    project = None
    tune_id = parts_dict.get("name")
    if not isinstance(tune_id, str):
        return "Expected string tune_id"

    tune_split = tune_id.split("/")
    if len(tune_split) == 1:
        pass
    elif len(tune_split) == 2:
        split_project, tune_id = tune_split
        project = split_project or project
    elif len(tune_split) == 3:
        split_entity, split_project, tune_id = tune_split
        project = split_project or project
        entity = split_entity or entity
    else:
        return "Expected tune_id in form of tune, project/tune, or entity/project/tune"
    parts_dict.update(dict(name=tune_id, project=project, entity=entity))


class AgentError(Exception):
    pass


@enum.unique
class CommandType(enum.IntEnum):
    RUN: int = 1
    STOP: int = 2
    EXIT: int = 3
    RESUME: int = 4


@enum.unique
class RunStatus(enum.IntEnum):
    QUEUED = 0
    RUNNING = 1
    STOPPED = 2
    DONE = 3
    ERRORED = 4


@dataclass
class Command:
    run_id: str
    type: CommandType
    config: Dict[str, Any] = None

    def __post_init__(self):
        self.type = getattr(CommandType, self.type)


@dataclass
class Job:
    command: Command
    run_id: str = None
    config: Dict[str, Any] = None
    status: RunStatus = None
    thread: str = None
    result: Any = None
    exception: str = None
    traceback = str = None

    def __post_init__(self):
        self.run_id = self.command.run_id
        self.config = self.command.config
        self.status = RunStatus.QUEUED


# TODO: change print to termerror / logger use
class Agent:
    def _init(self):
        # These are not in constructor so that Agent instance can be rerun
        self._run_threads = {}
        self._run_status = {}
        self._queue = queue.Queue()
        self._exit_flag = False
        self._exceptions = {}
        self._start_time = time.time()

    def _register(self, logger):
        print("Agent._register()")
        agent = self._api.register_agent(socket.gethostname(), tune_id=self._tune_id)
        self._agent_id = agent["id"]
        print("agent_id = {}".format(self._agent_id))

    def _setup(self, logger):
        print("Agent._setup()")
        self._init()
        parts = dict(entity=self._entity, project=self._project, name=self._tune_path)
        err = parse_tune_id(parts)
        if err:
            print(err)
            return
        entity = parts.get("entity") or self._entity
        project = parts.get("project") or self._project
        tune_id = parts.get("name") or self._tune_id
        if tune_id:
            os.environ[ml.env.TUNE_ID] = tune_id
        if entity:
            ml.env.set_entity(entity)
        if project:
            ml.env.set_project(project)
        if tune_id:
            self._tune_id = tune_id
        self._register(logger)

    def run(self):
        raise NotImplementedError()


def terminate_thread(thread, logger):
    if not thread.is_alive():
        return
    if hasattr(thread, "_terminated"):
        return
    thread._terminated = True
    tid = getattr(thread, "_thread_id", None)
    if tid is None:
        for k, v in threading._active.items():
            if v is thread:
                tid = k
    if tid is None:
        # This should never happen
        return
    print("Terminating thread: {}".format(tid))
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(Exception))
    if res == 0:
        # This should never happen
        return
    elif res != 1:
        # Revert
        print("Termination failed for thread {}".format(tid))
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
