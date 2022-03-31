from typing import TypeVar

from fregepoc.repositories.analyzers import BaseAnalyzer
from fregepoc.repositories.utils.analyzers import (
    FileInformationDict,
    generic_source_code_analysis,
)

ReturnType = TypeVar("ReturnType", bound=FileInformationDict)


class GenericAnalyzer(BaseAnalyzer[ReturnType]):
    def analyze(self, repo_file_obj):
        return generic_source_code_analysis(repo_file_obj)
