from collections import defaultdict
from typing import Dict, List

import optuna
from optuna.distributions import (
    CategoricalDistribution,
    IntUniformDistribution,
    UniformDistribution,
)

from manta_lab.tuning.interface.controller import TuningController
from manta_lab.tuning.interface.parameter import (
    Comparator,
    Goal,
    HyperParameter,
    ParameterType,
    SearchSpace,
    SearchSpaceAdapter,
)


class OptunaSearchSpaceAdapter(SearchSpaceAdapter):
    # https://optuna.readthedocs.io/en/stable/reference/distributions.html
    @staticmethod
    def convert(space: SearchSpace) -> Dict:
        optuna_space = {}
        for p in space.params:
            if p.type is ParameterType.INTEGER:
                optuna_param = IntUniformDistribution(int(p.min), int(p.max))
            elif p.type is ParameterType.FLOAT:
                optuna_param = UniformDistribution(float(p.min), float(p.max))
            elif p.type in (ParameterType.CATEGORICAL, ParameterType.DISCRETE):
                optuna_param = CategoricalDistribution(p.values)
            optuna_space[p.name] = optuna_param
        return optuna_space


# TODO: add argument list parse function
def create_tpe_sampler(settings: Dict, multivariate: bool):
    kwargs = dict()
    for k, v in settings.items():
        if k in ["n_startup_trials", "n_ei_candidates", "seed"]:
            kwargs[k] = int(v)
    if multivariate:
        kwargs["multivariate"] = multivariate
    kwargs["constant_liar"] = True

    return optuna.samplers.TPESampler(**kwargs)


def create_cmaes_sampler(settings: Dict):
    kwargs = dict()
    for k, v in settings.items():
        if k in ["restart_strategy", "sigma", "seed"]:
            kwargs[k] = int(v)

    return optuna.samplers.CmaEsSampler(**kwargs)


def create_random_sampler(settings: Dict):
    kwargs = {}
    for k, v in settings.items():
        if k in ["random_state"]:
            kwargs[k] = int(v)

    return optuna.samplers.RandomSampler(**kwargs)


def hash_parameters(params: Dict) -> str:
    # TODO: change hash algorithm
    params_str = [f"{k}:{v}" for k, v in params.items()]
    return ",".join(params_str)


class OptunaController(TuningController):
    def __init__(self) -> None:
        super().__init__()

        self.study = None
        self.search_space = None
        self._previous_jobs = list()
        self._optuna_numbers = defaultdict(list)

    def create_jobs(self, request):
        with self.lock:
            if self.study is None:
                self.search_space = SearchSpace.from_request(request)
                self.study = self._create_study(request["algorithm"], self.search_space)

            self._tell_optuna(request.get("previous_jobs", []))
            jobs = self._ask_optuna(request.get("num_target_jobs", 1))

            return jobs

    def _create_sampler(self, spec):
        name = spec["name"]
        settings = spec["settings"]

        if name == "tpe":
            sampler = create_tpe_sampler(settings, False)
        elif name == "multivariate-tpe":
            sampler = create_tpe_sampler(settings, True)
        elif name == "cmaes":
            sampler = create_cmaes_sampler(settings)
        elif name == "random":
            sampler = create_random_sampler(settings)

        return sampler

    def _create_study(self, algorithm_spec, search_space):
        sampler = self._create_sampler(algorithm_spec)
        direction = "maximize" if search_space.goal is Goal.MAXIMIZE else "minimize"

        study = optuna.create_study(sampler=sampler, direction=direction)
        return study

    def _ask_optuna(self, num_target_jobs: int) -> List:
        """ask optuna we want some number of jobs"""
        jobs = []
        for _ in range(num_target_jobs):
            distributions = OptunaSearchSpaceAdapter.convert(self.search_space)
            optuna_trial = self.study.ask(fixed_distributions=distributions)

            optuna_params = optuna_trial.params
            job_id = hash_parameters(optuna_params)
            jobs.append((job_id, optuna_params))
            self._optuna_numbers[job_id].append(optuna_trial.number)
        return jobs

    def _tell_optuna(self, previous_jobs):
        """tell optuna we already did some jobs"""
        for trial in previous_jobs:
            id = trial["id"]
            if id not in self._previous_jobs:
                assert id == hash_parameters(trial["parameters"])
                self._previous_jobs.append(id)

                metric = float(trial["metric"])
                optuna_trial_numbers = self._optuna_numbers[id]

                if optuna_trial_numbers:
                    trial_number = optuna_trial_numbers.pop(0)
                    self.study.tell(trial_number, metric)
                else:
                    raise ValueError("An unknown trial has been passed in the GetSuggestion request.")


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

    controller = OptunaController()
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
