from abc import abstractmethod
from typing import ParamSpec, Protocol, TypedDict, TypeVar, runtime_checkable

OutputType = TypeVar("OutputType", bound=TypedDict)
ParamsType = ParamSpec("P")


@runtime_checkable
class BaseAnalyzer(Protocol[ParamsType, OutputType]):
    @classmethod
    @abstractmethod
    def analyze(cls, *args: ParamsType.args, **kwargs: ParamsType.kwargs) -> OutputType:
        ...
