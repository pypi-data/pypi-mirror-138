import threading
import time
from collections import defaultdict
from typing import Callable, Dict, Mapping, TYPE_CHECKING

# TODO: dont want pandas dependencies
import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from manta_lab.base.packet import SummaryPacket
    from manta_lab.sdk.interface.interface import Interface


class NestedDict:
    def __init__(self) -> None:
        self._items = self._create_nested_dict()

    def _create_nested_dict(self):
        def _nested_dict():
            return defaultdict(_nested_dict)

        return _nested_dict()

    def __getitem__(self, key):
        return self._items.__getitem__(key)

    def __setitem__(self, key, val):
        self._items.__setitem__(key, val)

    def _update(self, _item, d):
        for k, v in d.items():
            if isinstance(v, dict):
                self._update(_item[k], v)
            else:
                _item[k] = v

    def update(self, d: Dict):
        self._update(self._items, d)

    @classmethod
    def from_flatten(cls, d: Dict):
        pass

    def _flatten(self, item, res, key):
        for k, v in item.items():
            new_key = ".".join([key, k])
            if isinstance(v, dict):
                self._flatten(v, res, new_key)
            else:
                res[new_key] = v

    def flatten(self):
        res = {}
        # self._flatten(self._items, res, "")
        for k, v in self._items.items():
            try:
                self._flatten(v, res, k)
            except AttributeError:
                res[k] = v
        return res


class Summary:
    """
    Tracks single values for each metric for each run.
    Summary can handle numpy arrays and PyTorch/TensorFlow tensors.
    Summary will give you values like min, mean, variance, and percentiles.

    By default, a metric's summary is the last value of its History.
    For example, `ml.log({'something': 0.1})` will add a new step to History and
    update Summary to the latest value.

    But, in some cases, it's more useful to have the maximum or minimum of a metric
    instead of the final value. You can set history manually
    `(ml.summary['accuracy'] = best_acc)`.

    Examples:
        ```python
        ml.init()

        best_accuracy = 0
        for epoch in range(epochs):
            test_loss, test_accuracy = function()
            if (test_accuracy > best_accuracy):
                ml.run.summary["best_accuracy"] = test_accuracy
                best_accuracy = test_accuracy
        ```

    """

    DEBOUNCE_SECONDS = 10

    def __init__(self, interface: "Interface"):
        self.interface = interface

        self._df = pd.DataFrame()
        self._items = NestedDict()
        self._thread = None
        self._shutdown = False

    def _summarize(self):
        df = self._df
        df = df.loc[:, ~df.columns.str.startswith("_")]
        if not df.empty:
            df = df.describe()
            df = df.replace({np.nan: None})
        return df.to_dict()

    def _exclude_media_items(self, d, res):
        for k, v in d.items():
            if isinstance(v, Mapping):
                if "_type" not in v:  # it means value is not media
                    res[k] = {}
                    self._exclude_media_items(v, res[k])
            else:
                res[k] = v

    def update(self, d: Dict):
        if len(d) == 0:
            return

        _d = {}
        self._exclude_media_items(d, _d)

        # update nested dict
        self._items.update(_d)
        flatten_items = self._items.flatten()

        # update table
        # TODO: this logic can make too many rows
        self._df = self._df.append(flatten_items, ignore_index=True)

        # TODO: if rows are too long...

    def flush(self):
        try:
            summary = self._summarize()
        except ValueError:
            pass
        else:
            self.interface.publish_summary(summary)

    def start(self) -> None:
        if self._thread is None:
            self._shutdown = False
            self._thread = threading.Thread(target=self._thread_body)
            self._thread.name = "SummaryThread"
            self._thread.daemon = True

        if not self._thread.is_alive():
            self._thread.start()

    def shutdown(self) -> None:
        self._shutdown = True
        try:
            if self._thread is not None:
                self._thread.join()
        finally:
            self._thread = None

    def _thread_body(self) -> None:
        while True:
            self.flush()

            # debouncing
            seconds = 0
            while seconds < self.DEBOUNCE_SECONDS:
                time.sleep(1)
                seconds += 1
                if self._shutdown:
                    self.flush()
                    return


if __name__ == "__main__":
    netsted = NestedDict()
    netsted["a"]["b"]["c"]["d"] = 0.3
    netsted.update({"a": {"b": {"d": 0.1}}})

    netsted.flatten()

    netsted.update({"b": 3})
    netsted.flatten()

    summary = Summary()
    summary.update({"a": {"b": {"d": 0.1}}})
    summary.update({"a": {"b": {"d": 0.2}}})
    summary.update({"a": {"b": {"d": 0.3}}})
    summary.update({"a": {"b": {"d": 0.4}}})
    summary.update({"a": {"b": {"d": 0.5}}})

    summary = Summary()
    summary.update({"loss": 0.1, "ttt": 0.5})
    summary.update({"loss": 0.2, "ttt": 0.4})
    summary.update({"loss": 0.3, "ttt": 0.3})
    summary.update({"loss": 0.4, "ttt": 0.2})
    summary.update({"loss": 0.5, "ttt": 0.1})
    print(summary.summarize())
