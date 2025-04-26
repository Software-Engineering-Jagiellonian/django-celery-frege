from frege.analyzers.core.base import AnalyzerFactory
from frege.analyzers.core.generic import GenericAnalyzer
from frege.repositories.constants import ProgrammingLanguages


@AnalyzerFactory.register(ProgrammingLanguages.RUST)
class RustAnalyzer(GenericAnalyzer):
    """Analyzer for Rust source files using generic metrics."""

    pass
