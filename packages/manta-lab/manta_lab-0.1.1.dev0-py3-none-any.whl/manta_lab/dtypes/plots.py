import os
from typing import Dict, List, Optional, Sequence, Tuple, TYPE_CHECKING, Union

import manta_lab.util as manta_util
from manta_lab.dtypes._interface import (
    BatchableMedia,
    LogUnit,
    Media,
    MEDIA_TEMP_DIR,
)
from manta_lab.dtypes.type_util import (
    matplotlib_contains_images,
    matplotlib_to_plotly,
)

if TYPE_CHECKING:
    import numpy as np

    from manta_lab.sdk.manta_run import Run


class Histogram(LogUnit):
    """manta_lab for histograms.

    This object works just like numpy's histogram function
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html

    Examples:
        Easy initialize from a sequence
        ```python
        manta_lab.Histogram([1,2,3])
        ```

        Efficiently initialize from np.histogram.
        ```python
        import numpy as np

        hist = np.histogram([1,2,3])
        manta_lab.Histogram(array=hist)
        ```
    """

    MAX_LENGTH: int = 512

    _log_type = "histogram"

    # from arguments
    _num_bins: int
    # from __init__
    _histogram: Optional[List]
    _bins: Optional[List]

    def __init__(
        self,
        seq_or_numpy: Union[Sequence, "np.ndarray"],
        num_bins: int = 16,
    ) -> None:

        self._num_bins = num_bins

        self._histogram = None
        self._bins = None

        if isinstance(seq_or_numpy, List):
            self._init_from_sequence(seq_or_numpy)
        else:
            self._init_from_numpy(seq_or_numpy)

        if len(self._histogram) > self.MAX_LENGTH:
            raise ValueError("The maximum length of a histogram is %i" % self.MAX_LENGTH)
        if len(self._histogram) + 1 != len(self._bins):
            raise ValueError("len(bins) must be len(histogram) + 1")

    def _create_np_histogram(self, array):
        np = manta_util.get_module("numpy", required="Auto creation of histograms requires numpy")

        histogram, bins = np.histogram(array, bins=self._num_bins)
        return histogram, bins

    def _init_from_sequence(self, sequence):
        histogram, bins = self._create_np_histogram(sequence)

        self._histogram = histogram.tolist()
        self._bins = bins.tolist()

    def _init_from_numpy(self, array):
        if len(array) != 2:
            array = self._create_np_histogram(array)

        histogram, bins = array
        # TODO: if user's array input is list, this will cause Error
        self._histogram = histogram.tolist()
        self._bins = bins.tolist()

    def to_json(self) -> dict:
        return {
            "_type": self._log_type,
            "values": self._histogram,
            "bins": self._bins,
        }


class Plotly(Media):
    _log_type = "plotly"

    def __init__(
        self,
        plotly_or_matplotlib,
    ) -> None:
        typename = manta_util.get_object_typename(plotly_or_matplotlib)

        if manta_util.is_plotly_figure_typename(typename):
            plot = plotly_or_matplotlib
        else:
            if manta_util.is_matplotlib_typename(typename):
                plot = self._init_from_matplotlib(plotly_or_matplotlib)
            else:
                raise ValueError("plots must be plotly or matplotlib convertible to plotly via mpl_to_plotly")

        self._init_from_plotly(plot)

    def _init_from_matplotlib(self, matplot):
        if matplotlib_contains_images(matplot):
            raise ValueError("Plotly doesnt support converting matplotlib containing images.")

        plot = matplotlib_to_plotly(matplot)
        return plot

    def _init_from_plotly(self, plot):
        temp_path = os.path.join(MEDIA_TEMP_DIR.name, manta_util.generate_id() + ".plotly.json")
        plot = plot.to_plotly_json()
        manta_util.write_json(temp_path, plot)
        self._set_file(temp_path, is_tmp=True, extension=".plotly.json")

    @staticmethod
    def get_media_subdir() -> str:
        return os.path.join("media", "plotly")

    def to_json(self) -> dict:
        json_dict = super().to_json()
        json_dict["_type"] = self._log_type
        return json_dict


class Bokeh:
    pass


class Matplotlib:
    """
    will be converted into plotly
    """

    pass
