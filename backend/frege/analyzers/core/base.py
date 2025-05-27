from abc import abstractmethod
from collections import defaultdict
from typing import (
    Callable,
    ClassVar,
    DefaultDict,
    Optional,
    Protocol,
    Type,
    TypedDict,
    TypeVar,
    runtime_checkable,
)

from frege.repositories.constants import ProgrammingLanguages
from frege.repositories.models import RepositoryFile

# Type variable for OutputType, which is a TypedDict.
OutputType = TypeVar("OutputType", bound=TypedDict)


@runtime_checkable
class BaseAnalyzer(Protocol[OutputType]):
    """
    A protocol for all analyzers in the system.

    This protocol defines the interface for language-specific file analysis classes.

    Attributes:
        None
    """

    @abstractmethod
    def analyze(self, repo_file_obj: RepositoryFile) -> OutputType:
        """
        Analyzes a repository file according to its specific programming language.

        Args:
            repo_file_obj (RepositoryFile): The repository file object to analyze.

        Returns:
            OutputType: The result of the analysis.
        """
        ...


class AnalyzerFactory:
    """
    A factory class for creating analyzer instances corresponding to specific programming languages.

    This singleton class manages the creation of analyzers for different programming languages.

    Attributes:
        analyzers (DefaultDict[str, list[Type[BaseAnalyzer]]]): A dictionary storing lists of analyzer classes 
            for each programming language.
    """

    __instance: Optional["AnalyzerFactory"] = None

    analyzers: ClassVar[DefaultDict[str, list[Type[BaseAnalyzer]]]] = defaultdict(list)

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def make_analyzers(
        cls, programming_language: ProgrammingLanguages
    ) -> list[BaseAnalyzer]:
        """
        Creates a list of analyzer instances for a given programming language.

        Args:
            programming_language (ProgrammingLanguages): The programming language for which to create analyzers.

        Returns:
            list[BaseAnalyzer]: A list of analyzer instances.
        """
        return [
            analyzer_cls()
            for analyzer_cls in cls.analyzers[programming_language]
        ]

    @classmethod
    def has_analyzers(cls, programming_language: ProgrammingLanguages) -> bool:
        """
        Checks if analyzers are registered for the specified programming language.

        Args:
            programming_language (ProgrammingLanguages): The programming language to check.

        Returns:
            bool: True if analyzers are registered for the language, False otherwise.
        """
        return bool(cls.analyzers[programming_language])

    @classmethod
    def register(
        cls, programming_language: ProgrammingLanguages
    ) -> Callable[[Type[BaseAnalyzer]], Type[BaseAnalyzer]]:
        """
        Registers an analyzer class for the specified programming language.

        Args:
            programming_language (ProgrammingLanguages): The programming language to register the analyzer for.

        Returns:
            Callable[[Type[BaseAnalyzer]], Type[BaseAnalyzer]]: A decorator that registers the analyzer class.
        """

        def wrapper(analyzer_cls: BaseAnalyzer) -> BaseAnalyzer:
            cls.analyzers[programming_language].append(analyzer_cls)
            return analyzer_cls

        return wrapper
