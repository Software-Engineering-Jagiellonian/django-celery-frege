from frege.analyzers.core.base import AnalyzerFactory
from frege.analyzers.core.generic import GenericAnalyzer
from frege.repositories.constants import ProgrammingLanguages


@AnalyzerFactory.register(ProgrammingLanguages.SWIFT)
class SwiftAnalyzer(GenericAnalyzer):
    """Analyzer for Swift source files using generic metrics."""

    pass
