from frege.analyzers.core.base import AnalyzerFactory
from frege.analyzers.core.generic import GenericAnalyzer
from frege.repositories.constants import ProgrammingLanguages


@AnalyzerFactory.register(ProgrammingLanguages.CPP)
class CppAnalyzer(GenericAnalyzer):
    """
    Analyzer for C++ source files.

    This class extends `GenericAnalyzer` and is registered in the `AnalyzerFactory`
    to handle analysis of files written in the C++ programming language.
    """
    pass
