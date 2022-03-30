from abc import abstractmethod
from collections import defaultdict
from typing import (
    Protocol,
    TypedDict,
    TypeVar,
    runtime_checkable,
    ClassVar,
    Type,
    Callable,
    DefaultDict,
)

from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.models import RepositoryFile

OutputType = TypeVar("OutputType", bound=TypedDict)


@runtime_checkable
class BaseAnalyzer(Protocol[OutputType]):
    """
    The base protocol class for all the analyzers present in the system.
    """

    @abstractmethod
    def analyze(self, repo_file_obj: RepositoryFile) -> OutputType:
        """
        A method performing language-specific file analysis.
        """
        ...


class AnalyzerFactory:
    """
    The factory for creating the analyzer instances corresponding to the particular programming languages.
    """

    analyzers: ClassVar[DefaultDict[str, list[Type[BaseAnalyzer]]]] = defaultdict(list)

    @classmethod
    def make_analyzers(
        cls, programming_language: ProgrammingLanguages
    ) -> list[BaseAnalyzer]:
        """
        Creates a list analyzers instances assigned for a given programming language.

        :param programming_language: The programming language whose analyzers will get returned.
        :return: The analyzer instances list.
        """
        return [analyzer_cls() for analyzer_cls in cls.analyzers[programming_language]]

    @classmethod
    def register(
        cls, programming_language: ProgrammingLanguages
    ) -> Callable[[Type[BaseAnalyzer]], Type[BaseAnalyzer]]:
        """
        Assigns an analyzer class to a given programming language.

        :param programming_language: The programming language the analyzer class will get assigned to.
        :return: A wrapper function.
        """

        def wrapper(analyzer_cls: BaseAnalyzer):
            cls.analyzers[programming_language].append(analyzer_cls)
            return analyzer_cls

        return wrapper
