from frege.analyzers.core.base import AnalyzerFactory
from frege.analyzers.core.generic import GenericAnalyzer
from frege.repositories.constants import ProgrammingLanguages


@AnalyzerFactory.register(ProgrammingLanguages.PHP)
class PhpAnalyzer(GenericAnalyzer):
    """
    Analyzer for PHP source files.

    Uses GenericAnalyzer to extract standard code metrics.
    """
    pass
