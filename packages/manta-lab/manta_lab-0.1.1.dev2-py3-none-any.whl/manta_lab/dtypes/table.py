import os
from numbers import Number
from typing import Callable, Dict, List, Optional, Sequence, Tuple, TYPE_CHECKING, Union

import pandas as pd

import manta_lab.util as manta_util
from manta_lab.dtypes._interface import Media, MEDIA_TEMP_DIR

# TODO: im not sure using pd.DataFrame fully is correct way for Manta-Lab
# this can cause various dependency problems for users


class Table(Media):
    """The Table class is used to display and analyze tabular data.

    Tables support numerous types of data
    scalar values, strings, numpy arrays, and manta extended Media types.
    This means you can embed `Images`, `Video`, `Audio`, and other subclasses of `manta_lab.data_types.Media`

    ```python
    import pandas as pd
    import manta_lab as ml

    data = {“student”: [“yj”, “jw”, “wq”],
            “score”: [90, 100, 70]}
    df = pd.DataFrame(data)

    tb = ml.Table(data=df)
    assert all(tb.get_column(“student”) == df[“student”])
    assert all(tb.get_column(“score”) == df[“score”])
    ```

    Users can also incrementally add data to the Tables using:
    `add_data`, `add_column`, and `add_computed_column` functions
    to add rows, columns and columns calculated from data in other columns, respectively

    ```python
    import manta_lab as ml

    tb = ml.Table(columns=[“student”])
    students = [“yejin”, “joowon”]

    [tb.add_data(student) for student in students]
    assert tb.get_column(“student”) == students

    def get_user_name_length(index, row):
        return {“len_name”: len(row[“student”])}
    tb.add_computed_columns(get_user_name_length)
    assert tb.get_column(“len_name”) == [5, 6]
    ```

    Tables added directly to runs as above create corresponding Table Visualizer in the
    Workspace that can be used for further analysis and reports export.

    Tables added to artifacts can be viewed in the Artifact Tab and will render
    an equivalent Table Visualizer directly in the artifact browser.

    Arguments:
        columns: (List[str]) Names of the columns in the table.
            Defaults to [“Input”, “Output”, “Expected”].
        data: (List[List[Any]]) 2D row-oriented array of values.
        dataframe: (pandas.DataFrame) DataFrame object used to create the table.
            When set, `data` and `columns` arguments are ignored.
    """

    # bigger max rows and artifacts needed
    MAX_ROWS = 3000
    MAX_ARTIFACT_ROWS = 60000

    _log_type = "table"

    _df: pd.DataFrame

    def __init__(
        self,
        columns=None,
        data=None,
        dataframe=None,
    ):
        # TODO: currently, all None values are accepted. But will need column policy for None acceptance.
        super().__init__()

        self._df = None

        # if dataframe is set,  `data` and `columns` arguments will be ignored.
        if dataframe is not None:
            self._init_from_dataframe()
        else:
            if data is not None:
                if manta_util.is_numpy_array(data) or isinstance(data, List):
                    self._init_from_sequence(data, columns)
                elif manta_util.is_pandas_data_frame(data):
                    self._init_from_dataframe(data, columns)
                else:
                    raise AttributeError("manta_lab.Table accepts pd.DataFrame, numpy.ndarray, list")
            # TODO: Default empty case, need some tests
            else:
                self._init_from_sequence([], columns)

    def _init_from_sequence(self, data, columns):
        self._df = pd.DataFrame(data, columns=columns)

    def _init_from_dataframe(self, dataframe):
        self._df = dataframe

    @classmethod
    def from_json(cls):
        # TODO: more complex than other dtypes, skip for now and implement later
        raise NotImplementedError()

    def to_json(self) -> Dict:
        json_dict = super().to_json()
        json_dict.update(
            {
                "_type": Table._log_type,
                "columns": self.columns,
                "contents": self.contents(),
                "ncols": len(self._df.columns),
                "nrows": len(self._df),
                "column_types": self.dtypes,
            }
        )
        return json_dict

    def bind_run(
        self,
        run,
    ) -> None:
        super().bind_run(run)

        def bind_elementwise(each):
            if hasattr(each, "bind_run"):
                each.bind_run(run)

        self._df.applymap(bind_elementwise)

    def _upload_table_contents(self, key, step):
        def upload_elementwise(each):
            if hasattr(each, "upload_file"):
                each.upload_file(key, step)

        self._df.applymap(upload_elementwise)

    def _serialize_table_contents(self):
        def serialize_elementwise(each):
            if hasattr(each, "run"):
                relpath = os.path.relpath(each.path, each.run.dir)
                value = {
                    "_type": each._log_type,
                    "path": f"{each.run.run_id}/{relpath}",
                }
            else:
                value = each
            return value

        self._df = self._df.applymap(serialize_elementwise)

    def upload_file(self, key, step):
        self._upload_table_contents(key, step)
        self._serialize_table_contents()

        data = {"columns": self.columns, "contents": self.contents()}
        path = os.path.join(MEDIA_TEMP_DIR.name, manta_util.generate_id() + ".table.json")
        manta_util.write_json(path, data)
        self._set_file(path, is_tmp=True, extension=".table.json")

        super().upload_file(key, step)

    @classmethod
    def get_media_subdir(cls):
        return os.path.join("media", "table")

    def add_data(self, *data):
        """Add a row of data to the table. Argument length should match column length"""

        if isinstance(data, str or Number):
            data = [data]

        columns = self.columns
        if len(data) != len(columns):
            raise ValueError(f"This table expects {len(columns)} columns: {columns}, found {len(data)}")

        if isinstance(data, Dict) or manta_util.is_pandas_data_frame(data):
            pass
        elif isinstance(data, (Tuple, List)) or manta_util.is_numpy_array(data):
            data = {columns[idx]: v for idx, v in enumerate(data)}
        else:
            raise AttributeError("add_data only accepts pd.DataFrame, np.ndarray, Dict and List")
        self._df = self._df.append(data, ignore_index=True)

    def add_column(self, name, data):
        assert isinstance(name, str) and name not in self.columns
        assert isinstance(data, list) or manta_util.is_numpy_array(data)
        self._df[name] = data

    def add_computed_columns(self, fn: Callable):
        """Adds one or more computed columns based on existing data

        Args:
            fn: A function which accepts one or two parameters, ndx (int) and row (dict),
                which is expected to return a dict representing new columns for that row, keyed
                by the new column names.

                `ndx` is an integer representing the index of the row. Only included if `include_ndx`
                      is set to `True`.

                `row` is a dictionary keyed by existing columns
        """
        fn_res = []
        for idx, row in self._df.iterrows():
            res = fn(idx, row)
            fn_res.append(res)
        fn_res = pd.DataFrame(fn_res)

        self._df = pd.concat([self._df, fn_res], axis=1)

    def get_column(self, name, convert_to=None):
        """Retrieves a column of data from the table

        Arguments
            name: (str) - the name of the column
            convert_to: (str, optional)
                - "numpy": will convert the underlying data to numpy object
        """
        assert name in self.columns
        assert convert_to in [None, "numpy"]

        data = self._df[name]
        if convert_to == "numpy":
            data = data.values
        else:
            data = data.values.tolist()
        return data

    def apply(self, *args, **kwargs):
        return self._df.apply(*args, **kwargs)

    def applymap(self, *args, **kwargs):
        return self._df.applymap(*args, **kwargs)

    @property
    def loc(self):
        return self._df.loc

    @property
    def iloc(self):
        return self._df.iloc

    @property
    def columns(self):
        return self._df.columns.values.tolist()

    @property
    def dtypes(self):
        # TODO: one column can have more than one dtype.
        #       need to make decision we accept multiple dtypes for each column.
        result = []
        for _, col in self._df.items():
            item = col.iloc[0]
            try:
                _type = item["_type"]
            except TypeError:
                _type = type(item).__name__
            result.append(_type)
        return result

    def contents(self, max_rows=None, warn=True):
        max_rows = max_rows or Table.MAX_ROWS
        if len(self._df) > max_rows and warn:
            print("manta_lab.Table can write %i rows." % max_rows)
        return self._df.loc[:max_rows, :].values.tolist()

    def __getattr__(self, key):
        return getattr(self._df, key)
