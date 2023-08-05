import enum
from typing import Dict, List, Union


@enum.unique
class Goal(enum.Enum):
    MAXIMIZE = enum.auto()
    MINIMIZE = enum.auto()


class ParameterType(enum.Enum):
    INTEGER = enum.auto()
    FLOAT = enum.auto()
    CATEGORICAL = enum.auto()
    DISCRETE = enum.auto()


@enum.unique
class Comparator(enum.Enum):
    EQUAL = enum.auto()
    LESS = enum.auto()
    GREATER = enum.auto()


class HyperParameter:
    def __init__(
        self,
        type: ParameterType,
        name: str,
        min: Union[int, float],
        max: Union[int, float],
        values: List,
        step: int,
    ) -> None:
        self.type = type
        self.name = name
        self.min = min
        self.max = max
        self.values = values
        self.step = step

    @classmethod
    def integer(cls, name, min, max, values, step):
        kwargs = locals()
        kwargs.pop("cls")
        return cls(ParameterType.INTEGER, **kwargs)

    @classmethod
    def float(cls, name, min, max, values, step):
        kwargs = locals()
        kwargs.pop("cls")
        return cls(ParameterType.FLOAT, **kwargs)

    @classmethod
    def categorical(cls, name, min, max, values, step):
        kwargs = locals()
        kwargs.pop("cls")
        return cls(ParameterType.CATEGORICAL, **kwargs)

    @classmethod
    def discrete(cls, name, min, max, values, step):
        kwargs = locals()
        kwargs.pop("cls")
        return cls(ParameterType.DISCRETE, **kwargs)

    @classmethod
    def from_request_param(cls, param: Dict):
        name, info = param

        param_cls, _type = cls.infer_value_type(info)
        kwargs = dict(
            name=name,
            min=info.get("min"),
            max=info.get("max"),
            values=info.get("values"),
            step=info.get("step"),
        )

        if _type is ParameterType.INTEGER:
            if not info.get("step"):
                kwargs["step"] = 1

        return param_cls(**kwargs)

    @staticmethod
    def infer_value_type(info):
        _type = info.get("type")
        if _type:
            _type = getattr(ParameterType, _type.upper())
        # TODO: whats difference btw DISCRETE, CATEGORICAL
        # TODO: whats difference btw INTEGER, DOUBLE
        else:
            values_ = info.get("values")
            min_ = info.get("min")
            max_ = info.get("max")

            if values_:
                _type = ParameterType.DISCRETE
            elif min_ or max_:
                if min_ == int(min_) and max_ == int(max_):
                    _type = ParameterType.INTEGER
                else:
                    _type = ParameterType.FLOAT

        _param_cls = getattr(HyperParameter, _type.name.lower())
        return _param_cls, _type

    def __str__(self):
        if self.type in [ParameterType.INTEGER, ParameterType.DOUBLE]:
            return "HyperParameter(name: {}, type: {}, min: {}, max: {}, step: {})".format(
                self.name, self.type, self.min, self.max, self.step
            )
        else:
            return "HyperParameter(name: {}, type: {}, values: {})".format(self.name, self.type, ", ".join(self.values))


class SearchSpace:
    def __init__(self) -> None:
        self.goal = None
        self.params = list()

    # TODO: add iterator

    def set_goal(self, goal):
        assert goal.upper() in ["MAXIMIZE", "MINIMIZE"]
        self.goal = getattr(Goal, goal.upper())

    def add_param(self, param: HyperParameter):
        assert isinstance(param, HyperParameter)
        self.params.append(param)

    @classmethod
    def from_request(cls, req):
        space = cls()
        space.set_goal(req["algorithm"]["metric"]["goal"])
        for p in req["parameters"].items():
            space.add_param(HyperParameter.from_request_param(p))
        return space


class SearchSpaceAdapter:
    def convert():
        raise NotImplementedError()
