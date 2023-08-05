from typing import Dict, Optional, Union

from manta_lab.tuning.internal.controller import ControllerFactory


def create_controller(config: Dict):
    return ControllerFactory.create(config)


def controller(
    tune_id_or_config: Optional[Union[str, Dict]] = None,
    entity: Optional[str] = None,
    project: Optional[str] = None,
):
    """Public tune controller constructor.

    Usage:
        import manta_client
        tuner = manta_client.controller(...)
        print(tuner.tune_config)
        print(tuner.tune_id)
        tuner.configure_search(...)
        tuner.configure_stopping(...)
    """
    if isinstance(tune_id_or_config, Dict):
        c = create_controller(tune_id_or_config)
    return c
