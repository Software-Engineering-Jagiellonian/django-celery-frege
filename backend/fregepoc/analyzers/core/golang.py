from typing import TypedDict

import lizard

from fregepoc.analyzers.core.base import AnalyzerFactory, BaseAnalyzer
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.utils.analyzers import repo_file_content


class GolangFileAnalysisResult(TypedDict):
    lines_of_code: int
    token_count: int
    average_lines_of_code: int
    average_token_count: int
    average_cyclomatic_complexity: int
    average_parameter_count: int
    number_of_functions: int


@AnalyzerFactory.register(ProgrammingLanguages.GOLANG)
class GolangAnalyzer(BaseAnalyzer[GolangFileAnalysisResult]):
    def analyze(self, repo_file_obj):
        with repo_file_content(repo_file_obj) as file_content:
            analysis_result = lizard.analyze_file.analyze_source_code(
                ".go", file_content
            )

            return {
                "lines_of_code": analysis_result.nloc,
                "token_count": analysis_result.token_count,
                "average_lines_of_code": analysis_result.average_nloc,
                "average_token_count": analysis_result.average_token_count,
                "average_cyclomatic_complexity": analysis_result.average_cyclomatic_complexity,
                "average_parameter_count": analysis_result.functions_average(
                    "parameter_count"
                ),
                "number_of_functions": len(analysis_result.function_list)
            }
