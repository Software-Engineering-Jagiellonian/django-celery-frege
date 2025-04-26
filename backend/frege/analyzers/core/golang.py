from frege.analyzers.core.base import AnalyzerFactory
from frege.analyzers.core.generic import GenericAnalyzer
from frege.repositories.constants import ProgrammingLanguages


@AnalyzerFactory.register(ProgrammingLanguages.GOLANG)
class GolangAnalyzer(GenericAnalyzer):
    """
    Analyzer for Go source files.

    Registered in the AnalyzerFactory and uses GenericAnalyzer 
    to compute standard code metrics.
    """
    
    pass
