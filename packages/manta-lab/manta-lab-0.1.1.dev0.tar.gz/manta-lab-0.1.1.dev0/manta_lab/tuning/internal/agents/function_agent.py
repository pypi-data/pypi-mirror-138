# -*- coding: utf-8 -*-
import os
import queue
import socket
import threading
import time

import manta_lab as ml
from manta_lab.tuning.interface.agent import (
    Agent,
    Command,
    CommandType,
    Job,
    RunStatus,
    terminate_thread,
)


# TODO: api.register_agent, request_tune_schedule
# TODO: os.environ set needed?
class FunctionAgent(Agent):

    FLAPPING_MAX_SECONDS = 60
    FLAPPING_MAX_FAILURES = 3
    MAX_INITIAL_FAILURES = 5

    def __init__(self, api, tune_id=None, entity=None, project=None, function=None, count=None, logger=None):
        self._api = api
        self._tune_id = tune_id
        self._entity = entity
        self._project = project
        self._function = function
        self._max_counts = count
        self._logger = logger

        self._agent_id = None
        self._max_initial_failures = ml.env.get_agent_max_initial_failures(self.MAX_INITIAL_FAILURES)

    def _init(self):
        self._jobs = {}
        self._queue = queue.Queue()
        self._exit_flag = False
        self._exceptions = {}
        self._start_time = time.time()

    def _register(self):
        print("Agent._register()")
        agent = self._api.register_agent(socket.gethostname(), tune_id=self._tune_id)
        self._agent_id = agent["id"]
        print("agent_id = {}".format(self._agent_id))

    def _setup(self):
        print("Agent._setup()")
        self._init()
        parts = dict(entity=self._entity, project=self._project, name=self._tune_id)
        err = ml.util.parse_tune_id(parts)
        if err:
            print(err)
            return
        # TODO: if user only specified tune_id, these values should be backpropagated. using env
        self._entity = parts.get("entity") or self._entity
        self._project = parts.get("project") or self._project
        self._tune_id = parts.get("name") or self._tune_id
        self._register()

    def _stop_run(self, run_id):
        print("Stopping run {}.".format(run_id))
        self._jobs[run_id].status = RunStatus.STOPPED
        thread = self._jobs.get(run_id).thread
        if thread:
            terminate_thread(thread, self.logger)

    def _stop_all_runs(self):
        print("Stopping all runs.")
        for run in list(self._jobs.keys()):
            self._stop_run(run)

    def _exit(self):
        self._stop_all_runs()
        self._exit_flag = True
        # terminate_thread(self._main_thread)

    def _subscribe_tuner(self):
        while True:
            if self._exit_flag:
                return

            current_jobs = {
                job_id: True
                for job_id, job in self._jobs.items()
                if job.status in (RunStatus.QUEUED, RunStatus.RUNNING)
            }
            commands = self._api.request_tune_schedule(self._agent_id, {}, current_jobs)

            if commands:
                command = Command(**commands[0])
                job = Job(command=command)
                print("command received: {}".format(command))
                if command.type in [CommandType.RUN, CommandType.RESUME]:
                    job.status = RunStatus.QUEUED
                    self._queue.put(job)
                    self._jobs[job.run_id] = job
                elif command.type is CommandType.STOP:
                    self._stop_run(job.run_id)
                elif command.type is CommandType.EXIT:
                    self._exit()
                    return
            time.sleep(5)

    def _run_jobs_from_queue(self):
        global _INSTANCES
        _INSTANCES += 1
        try:
            waiting = False
            count = 0
            while True:
                if self._exit_flag:
                    return
                try:
                    try:
                        job = self._queue.get(timeout=5)
                        if self._exit_flag:
                            print("Exiting main loop due to exit flag.")
                            print("tune Agent: Exiting.")
                            return
                    except queue.Empty:
                        if not waiting:
                            print("Paused.")
                            print("tune Agent: Waiting for job.")
                            waiting = True
                        time.sleep(5)
                        if self._exit_flag:
                            print("Exiting main loop due to exit flag.")
                            print("tune Agent: Exiting.")
                            return
                        continue

                    if waiting:
                        print("Resumed.")
                        print("Job received.")
                        waiting = False

                    count += 1
                    run_id = job.run_id
                    if self._jobs[run_id] is RunStatus.STOPPED:
                        continue

                    self._spawn_job_thread(job)
                    self._handle_run_status(job, count)
                    if self._exit_flag:
                        return

                except KeyboardInterrupt:
                    print("Ctrl + C detected. Stopping tune.")
                    self._exit()
                    return
                except Exception as e:
                    if self._exit_flag:
                        print("Exiting main loop due to exit flag.")
                        print("tune Agent: Killed.")
                        return
                    else:
                        raise e
        finally:
            _INSTANCES -= 1

    def _run_job(self, job):
        try:
            run_id = job.run_id
            config_file = os.path.join("manta", "tune-" + self._tune_id, "config-" + run_id + ".yaml")
            base_dir = os.environ.get(ml.env.BASE_DIR, "")
            tune_param_path = os.path.join(base_dir, config_file)
            ml.util.save_yaml(tune_param_path, job.config)
            # ml.sdk.manta_setup._setup(_reset=True)

            print("Agent Starting Run: {} with config:".format(run_id))
            for k, v in job.config.items():
                try:
                    print("\t{}: {}".format(k, v["value"]))
                except:
                    print("\t{}: {}".format(k, v))
            self._function()
            ml.finish()
        except KeyboardInterrupt as ki:
            print(ki)
            raise ki
        except Exception as e:
            ml.finish(exit_code=1)
            job = self._jobs[run_id]
            if job.status is RunStatus.RUNNING:
                job.status = RunStatus.ERRORED
                job.exception = e
                self._exceptions[run_id] = e
        finally:
            os.environ.pop(ml.env.EXPERIMENT_ID, None)
            os.environ.pop(ml.env.TUNE_ID, None)
            os.environ.pop(ml.env.TUNE_PARAM_PATH, None)

    def _spawn_job_thread(self, job):
        print("Spawning new thread for run {}.".format(job.run_id))
        thread = threading.Thread(target=self._run_job, args=(job,))
        thread.name = f"tune-{job.run_id}_runner"
        job.thread = thread
        thread.start()
        job.status = RunStatus.RUNNING
        thread.join()
        print("Thread joined for run {}.".format(job.run_id))

    def _handle_run_status(self, job, count):
        run_id = job.run_id
        if self._jobs[run_id] is RunStatus.RUNNING:
            self._jobs[run_id] = RunStatus.DONE
        elif self._jobs[run_id] is RunStatus.ERRORED:
            exc = self._exceptions[run_id]
            print("Run {} errored: {}".format(run_id, repr(exc)))
            print("Run {} errored: {}".format(run_id, repr(exc)))
            if os.getenv(ml.env.AGENT_DISABLE_FLAPPING) is True:
                self._exit_flag = True
                return
            elif (time.time() - self._start_time < self.FLAPPING_MAX_SECONDS) and (
                len(self._exceptions) >= self.FLAPPING_MAX_FAILURES
            ):
                msg = "Detected {} failed runs in the first {} seconds, killing tune.".format(
                    self.FLAPPING_MAX_FAILURES, self.FLAPPING_MAX_SECONDS
                )
                print(msg)
                print("To disable this check set MANTA_AGENT_DISABLE_FLAPPING=true")
                self._exit_flag = True
                return
            if self._max_initial_failures < len(self._exceptions) and len(self._exceptions) >= count:
                msg = "Detected {} failed runs in a row at start, killing tune.".format(self._max_initial_failures)
                print(msg)
                print("To change this value set MANTA_AGENT_MAX_INITIAL_FAILURES=val")
                self._exit_flag = True
                return

        if self._max_counts and self._max_counts == count:
            print("Exiting main loop because max count reached.")
            self._exit_flag = True
            return

    def run(self):
        print(
            "Starting tune agent: entity={}, project={}, count={}".format(self._entity, self._project, self._max_counts)
        )
        self._setup()
        self._subscribe_tuner_thread = threading.Thread(target=self._subscribe_tuner)
        self._subscribe_tuner_thread.daemon = True
        self._subscribe_tuner_thread.name = "tuner_subscribe_thread"
        self._subscribe_tuner_thread.start()
        self._run_jobs_from_queue()


_INSTANCES = 0


def is_running():
    return bool(_INSTANCES)
