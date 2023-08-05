from typing import Callable, Optional, Union
from urllib.parse import quote

import manta_lab as ml


def get_tune_url(api, tune_id):
    if api.api_key:
        project = api.project
        if not project:
            return
        return "{base}/{entity}/{project}/tune/{tune_id}".format(
            base=api.base_url,
            entity=quote(api.entity),
            project=quote(project),
            tune_id=quote(tune_id),
        )


def tune(
    tune: Union[dict, Callable],
    project: str,
    entity: Optional[str] = None,
) -> str:
    """
    Initialize a hyperparameter tuner.

    create tuner -> call agent

    Returns:
      tuner_id: str. A unique id for tuner.

    Examples:ƒ
        Basic usage
        ```python
        import manta_lab
        config = {
            "name": "awesome-tune",
            "metric": {"name": "accuracy", "goal": "maximize"},
            "method": "grid",
            "parameters": {
                "a": {
                    "values": [1, 2, 3, 4]
                }
            }
        }

        def my_train_func():
            manta_lab.init()
            a = manta_lab.config.a

            manta_lab.log({"a": a, "accuracy": a + 1})

        tune_id = manta_lab.tune(config)

        # run the tune
        manta_lab.runner(tune_id, function=my_train_func)
        ```
    """
    if callable(tune):
        tune = tune()

    setting = ml.Settings(project=project, entity=entity)

    api = ml.api.MantaAPI(settings=setting)
    tune_id = api.create_tuner(tune)  # TODO: returns warning message?

    print("Tuner created:", tune_id)
    tune_url = get_tune_url(api, tune_id)
    if tune_url:
        print("tune URL:", tune_url)
    return tune_id
