from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.core.generic import GenericAnalyzer
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.utils.analyzers import FileInformationDict


@AnalyzerFactory.register(ProgrammingLanguages.KOTLIN)
class KotlinAnalyzer(GenericAnalyzer[FileInformationDict]):
    pass
