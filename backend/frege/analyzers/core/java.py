from frege.analyzers.core.base import AnalyzerFactory
from frege.analyzers.core.generic import GenericAnalyzer
from frege.repositories.constants import ProgrammingLanguages


@AnalyzerFactory.register(ProgrammingLanguages.JAVA)
class JavaAnalyzer(GenericAnalyzer):
    """
    Analyzer for Java source files.

    Uses GenericAnalyzer to collect standard code metrics.
    """
    
    pass
