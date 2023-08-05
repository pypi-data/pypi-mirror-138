import queue
import socket
import threading
import time

from manta_lab.tuning.internal.integrations import (
    BayesianController,
    ChocolateController,
    HyperbandController,
    HyperOptController,
    OptunaController,
    RayController,
    SkOptController,
)


class ControllerFactory:
    @staticmethod
    def create(request):
        name = request["algorithm"]["name"]

        if name in ["tpe", "multivariate-tpe", "cmaes", "random"]:
            return OptunaController()
        elif name in ["bayesian"]:
            return BayesianController()
        elif name in ["choco-grid", "choco-random", "choco-quasirandom", "choco-bayesian", "choco-mocmaes"]:
            return ChocolateController()
        elif name in ["hyperband"]:
            return HyperbandController()
        elif name in ["hyperopt-tpe", "hyperopt-random"]:
            return HyperOptController()
        elif name in ["ray"]:  # Too many integrations here. need to get algorithm name in other param
            return RayController()
        elif name in []:
            return SkOptController()
        else:
            raise AttributeError("Wrong Algorithm name")


# TODO: this will be refactor later
class ControllerSerivce:
    def __init__(self, tune_id):
        self._tune_id = tune_id
        self._jobs = {}
        self._queue = queue.Queue()
        self._exit_flag = False
        self._start_time = time.time()
        self._controller_id = None

    def _register_controller(self):
        """Tell server controller starts running.
        tune_id, host, thread or process id
        """
        controller = self._api.register_controller(host=socket.gethostname(), tune_id=self._tune_id, process_id=123)
        self._controller_id = controller["id"]

    def _setup(self, req):
        self._register_controller()
        self._controller = ControllerFactory.create(req)

    def _thread_body(self):
        while True:
            if self._exit_flag:
                return

            requests = self._read_requests_from_queue()
            for req in requests:
                jobs = controller.create_jobs(req)
                self._publish_agent(jobs)

    def _publish_agent(self, jobs):
        pass

    def _read_requests_from_queue(self):
        return []

    def run(self, req):
        print("Starting tune controller: tune_id={}".format(self._tune_id))

        self._setup(req)
        self._thread_body()
        # self._tuner_thread = threading.Thread(target=self._thread_body)
        # self._tuner_thread.daemon = True
        # self._tuner_thread.name = f"controller_thread({self._tune_id})"
        # self._tuner_thread.start()


if __name__ == "__main__":
    req = {
        "algorithm": {
            "name": "tpe",
            "metric": {"name": "accuracy", "goal": "maximize"},
            "settings": {"n_startup_trials": 1},
        },
        "parameters": {
            "a": {"values": [1, 2, 3, 4]},
            "b": {"type": "integer", "min": 0, "max": 10},
            "c": {"type": "float", "min": -5, "max": 5},
            "d": {"values": [1, 2, 3, 4]},
        },
    }

    controller = ControllerFactory.create(req)
    job = controller.create_jobs(req)

    req2 = {
        "previous_jobs": [
            {
                "id": job[0][0],
                "metric": 10,
                "parameters": job[0][1],
            }
        ],
    }
    req2.update(req)
    job2 = controller.create_jobs(req2)
    controller.create_jobs(req)
