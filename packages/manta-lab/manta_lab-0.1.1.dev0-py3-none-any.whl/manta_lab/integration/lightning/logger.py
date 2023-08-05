import operator
import os
from argparse import Namespace
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
from weakref import ReferenceType

import torch.nn as nn
from pytorch_lightning import LightningModule
from pytorch_lightning.callbacks.model_checkpoint import ModelCheckpoint
from pytorch_lightning.loggers.base import LightningLoggerBase, rank_zero_experiment
from pytorch_lightning.utilities import _module_available, rank_zero_only
from pytorch_lightning.utilities.exceptions import MisconfigurationException
from pytorch_lightning.utilities.imports import _compare_version
from pytorch_lightning.utilities.warnings import rank_zero_warn

import manta_lab as ml
from manta_lab.sdk.manta_run import Run


class MantaLogger(LightningLoggerBase):
    # TODO: add doc

    _experiment: Optional[Run]
    _logged_model_time: Dict
    _checkpoint_callback: Callable

    def __init__(
        self,
        project: Optional[str] = None,
        entity: Optional[str] = None,
        name: Optional[str] = None,
        save_dir: Optional[str] = None,
        offline: Optional[bool] = False,
        id: Optional[str] = None,  # do we use?
        version: Optional[str] = None,  # do we use?
        log_model: Optional[bool] = False,
        prefix: Optional[str] = "",
        **kwargs,
    ):
        if offline:
            raise MisconfigurationException(
                "Currently, manta-lab doesnt support offline mode. We will implement it soon!"
            )
        if offline and log_model:
            raise MisconfigurationException(
                f"Providing log_model={log_model} and offline={offline} is an invalid configuration"
                " since model checkpoints cannot be uploaded in offline mode.\n"
                "Hint: Set `offline=False` to log your model."
            )

        super().__init__()
        self._project = project or "pl-undefined"
        self._entity = entity
        self._name = name
        self._save_dir = save_dir
        self._offline = offline
        self._version = version
        self._log_model = log_model
        self._prefix = prefix

        # TODO: offline to mode
        self.init_kwargs = dict(
            project=project,
            entity=entity,
            name=name,
            # id=version or id,
            # dir=save_dir,
            # mode=something
        )
        self.init_kwargs.update(**kwargs)

        self._id = self.init_kwargs.get("id")
        self._experiment = None
        self._logged_model_time = {}
        self._checkpoint_callback = None

    def __getstate__(self):
        state = self.__dict__.copy()
        state["_id"] = self._experiment.run_id if self._experiment is not None else None
        # for pickle
        state["_experiment"] = None
        return state

    @property
    @rank_zero_experiment
    def experiment(self) -> Run:
        if self._experiment is None:
            if ml.run is None:
                self._experiment = ml.init(**self.init_kwargs)
            else:
                rank_zero_warn(
                    "There is a manta run already in progress and newly created instances of `MantaLogger` will reuse"
                    " this run. If this is not desired, call `manta.finish()` before instantiating `MantaLogger`."
                )
                self._experiment = ml.run

        return self._experiment

    @rank_zero_only
    def log_hyperparams(self, params: Union[Dict[str, Any], Namespace]) -> None:
        """Record hyperparameters.
        Args:
            params: :class:`~argparse.Namespace` containing the hyperparameters
            args: Optional positional arguments, depends on the specific logger being used
            kwargs: Optional keywoard arguments, depends on the specific logger being used
        """
        params = self._convert_params(params)
        params = self._flatten_dict(params)
        params = self._sanitize_callable_params(params)
        self.experiment.update_config(params)

    @rank_zero_only
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None) -> None:
        """
        Records metrics.
        This method logs metrics as as soon as it received them. If you want to aggregate
        metrics for one specific `step`, use the
        :meth:`~pytorch_lightning.loggers.base.LightningLoggerBase.agg_and_log_metrics` method.
        Args:
            metrics: Dictionary with metric names as keys and measured quantities as values
            step: Step number at which the metrics should be recorded
        """
        assert rank_zero_only.rank == 0, "experiment tried to log from global_rank != 0"

        metrics = self._add_prefix(metrics)
        if step is not None:
            self.experiment.log({**metrics, "_trainer/global_step": step})
        else:
            self.experiment.log(metrics)

    @rank_zero_only
    def log_table(
        self,
        key: str,
        columns: List[str] = None,
        data: List[List[Any]] = None,
        dataframe: Any = None,
        step: Optional[int] = None,
    ) -> None:
        # TODO: Implement here after Table
        raise NotImplementedError()

    @rank_zero_only
    def log_text(
        self,
        key: str,
        columns: List[str] = None,
        data: List[List[str]] = None,
        dataframe: Any = None,
        step: Optional[int] = None,
    ) -> None:
        # TODO: Implement here after Table
        raise NotImplementedError()

    @rank_zero_only
    def log_image(self, key: str, images: List[Any], step: Optional[int] = None, **image_kwargs) -> None:
        """Log images (tensors, numpy arrays, PIL Images or file paths).
        Args:
            key: key
            images: can be captions, classes, box, masks
            step: step
        """
        # TODO: Implement here after Image
        raise NotImplementedError()

        # if not isinstance(images, list):
        #     raise TypeError(f'Expected a list as "images", found {type(images)}')

        # n = len(images)
        # for k, v in image_kwargs.items():
        #     if len(v) != n:
        #         raise ValueError(f"Expected {n} items but only found {len(v)} for {k}")

        # kwarg_list = [{k: image_kwargs[k][i] for k in image_kwargs.keys()} for i in range(n)]
        # metrics = {key: [ml.Image(img, **kwarg) for img, kwarg in zip(images, kwarg_list)]}
        # self.log_metrics(metrics, step)

    @rank_zero_only
    def log_graph(self, model: LightningModule, input_array=None) -> None:
        """Record model graph.
        Args:
            model: lightning model
            input_array: input passes to `model.forward`
        """
        # TODO: Implement here after Image
        pass

    @rank_zero_only
    def finalize(self, status: str) -> None:
        """Do any processing that is necessary to finalize an experiment.
        Args:
            status: Status that the experiment finished with (e.g. success, failed, aborted)
        """
        if self._checkpoint_callback:
            self._scan_and_log_checkpoints(self._checkpoint_callback)

    def after_save_checkpoint(self, checkpoint_callback: "ReferenceType[ModelCheckpoint]") -> None:
        """Called after model checkpoint callback saves a new checkpoint.
        Args:
            checkpoint_callback: the model checkpoint callback instance
        """
        if self._log_model == "all" or self._log_model is True and checkpoint_callback.save_top_k == -1:
            self._scan_and_log_checkpoints(checkpoint_callback)
        elif self._log_model is True:
            self._checkpoint_callback = checkpoint_callback

    @property
    def save_dir(self) -> Optional[str]:
        """Gets the save directory.
        Returns:
            The path to the save directory.
        """
        return self._save_dir

    @property
    def name(self) -> Optional[str]:
        """Gets the name of the experiment.
        Returns:
            The name of the experiment if the experiment exists else the name given to the constructor.
        """
        if self._experiment:
            return self._experiment.project
        else:
            return self._name or self._project

    @property
    def version(self) -> Optional[str]:
        """Gets the id of the experiment.
        Returns:
            The id of the experiment if the experiment exists else the id given to the constructor.
        """
        if self._experiment:
            return self._experiment.run_id
        else:
            return self._id

    def _get_checkpoint_data(checkpoint_callback: "ReferenceType[ModelCheckpoint]") -> Dict:
        keys = ["monitor", "mode", "save_last", "save_top_k", "save_weights_only", "_every_n_train_steps"]
        data = {}
        for key in keys:
            val = getattr(checkpoint_callback, key, None)
            if val:
                data[key] = val
        return data

    def _scan_and_log_checkpoints(self, checkpoint_callback: "ReferenceType[ModelCheckpoint]") -> None:
        # TODO: current artifact need more stabilizations
        raise NotImplementedError()

        checkpoints = {
            checkpoint_callback.last_model_path: checkpoint_callback.current_score,
            checkpoint_callback.best_model_path: checkpoint_callback.best_model_score,
            **checkpoint_callback.best_k_models,
        }

        _checkpoints = []
        for path, score in checkpoints.items():
            p = Path(path)
            if p.is_file():
                timestamp = p.stat().st_mtime
                _checkpoints.append((timestamp, path, score))
        checkpoints = sorted(_checkpoints)

        _checkpoints = []
        for ckpt in checkpoints:
            timestamp, path, _ = ckpt
            if path not in self._logged_model_time.keys() or self._logged_model_time[path] < timestamp:
                _checkpoints.append(ckpt)
        checkpoints = _checkpoints

        # log iteratively all new checkpoints
        for timestamp, path, score in checkpoints:
            metadata = {
                "score": score,
                "filename": Path(p).name,
                "lightning-model": self._get_checkpoint_dict(),
            }

            artifact = ml.Artifact(name=f"model-{self.experiment.run_id}", type="model", metadata=metadata)
            artifact.add_file(path, name="model.ckpt")
            lables = ["latest", "best"] if path == checkpoint_callback.best_model_path else ["latest"]
            self.experiment.log_artifact(artifact, labels=lables)

            self._logged_model_time[path] = timestamp
