from frege.analyzers.core.base import AnalyzerFactory
from frege.analyzers.core.generic import GenericAnalyzer
from frege.repositories.constants import ProgrammingLanguages


@AnalyzerFactory.register(ProgrammingLanguages.JS)
class JavascriptAnalyzer(GenericAnalyzer):
    """
    Analyzer for JavaScript source files.

    Uses GenericAnalyzer to collect standard code metrics.
    """
    pass
