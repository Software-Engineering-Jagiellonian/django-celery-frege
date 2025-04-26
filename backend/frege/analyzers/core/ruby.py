from frege.analyzers.core.base import AnalyzerFactory
from frege.analyzers.core.generic import GenericAnalyzer
from frege.repositories.constants import ProgrammingLanguages


@AnalyzerFactory.register(ProgrammingLanguages.RUBY)
class RubyAnalyzer(GenericAnalyzer):
    """Analyzer for Ruby source files using generic metrics."""

    pass
