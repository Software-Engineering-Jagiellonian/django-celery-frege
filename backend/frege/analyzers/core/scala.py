from frege.analyzers.core.base import AnalyzerFactory
from frege.analyzers.core.generic import GenericAnalyzer
from frege.repositories.constants import ProgrammingLanguages


@AnalyzerFactory.register(ProgrammingLanguages.SCALA)
class ScalaAnalyzer(GenericAnalyzer):
    """Analyzer for Scala source files using generic metrics."""
    pass
