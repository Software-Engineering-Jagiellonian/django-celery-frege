from frege.analyzers.core.base import AnalyzerFactory
from frege.analyzers.core.generic import GenericAnalyzer
from frege.repositories.constants import ProgrammingLanguages


@AnalyzerFactory.register(ProgrammingLanguages.TYPESCRIPT)
class TypescriptAnalyzer(GenericAnalyzer):
    """Analyzer for TypeScript source files using generic metrics."""

    pass
