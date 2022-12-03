from typing import TypedDict

import lizard

from fregepoc.analyzers.core.base import AnalyzerFactory, BaseAnalyzer
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.utils.analyzers import repo_file_content


class TypescriptFileAnalysisResult(TypedDict):
    lines_of_code: int
    token_count: int
    average_lines_of_code: float
    average_token_count: float
    average_cyclomatic_complexity: float


@AnalyzerFactory.register(ProgrammingLanguages.TYPESCRIPT)
class JavascriptAnalyzer(BaseAnalyzer[TypescriptFileAnalysisResult]):
    def get_analisys_results(self, res):
        return {
            "lines_of_code": res.nloc,
            "token_count": res.token_count,
            "average_lines_of_code": res.average_nloc,
            "average_token_count": res.average_token_count,
            "average_cyclomatic_complexity": res.average_cyclomatic_complexity,
        }

    def analyze(self, repo_file_obj):
        with repo_file_content(repo_file_obj) as file_content:
            result = lizard.analyze_file.analyze_source_code(
                ".ts", file_content
            )

            return self.get_analisys_results(result)
