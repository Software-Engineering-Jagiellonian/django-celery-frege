from typing import TypedDict

import lizard
import statistics

from fregepoc.analyzers.core.base import AnalyzerFactory, BaseAnalyzer
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.utils.analyzers import repo_file_content


class SwiftFileAnalysisResult(TypedDict):
    lines_of_code: int
    token_count: int
    function_count: int
    average_function_name_length: float
    average_lines_of_code: float
    average_token_count: float
    average_cyclomatic_complexity: float
    average_parameter_count: float


@AnalyzerFactory.register(ProgrammingLanguages.SWIFT)
class SwiftAnalyzer(BaseAnalyzer[SwiftFileAnalysisResult]):
    def analyze(self, repo_file_obj):
        with repo_file_content(repo_file_obj) as file_content:
            analysis_result = lizard.analyze_file.analyze_source_code(
                ".swift", file_content
            )

            def average_func_name_len(function_list):
                func_name_lengths = [len(func.name) for func in function_list]
                return statistics.fmean(func_name_lengths) if func_name_lengths else 0.0

            return {
                "lines_of_code": analysis_result.nloc,
                "token_count": analysis_result.token_count,
                "function_count": len(analysis_result.function_list),
                "average_function_name_length": average_func_name_len(analysis_result.function_list),
                "average_lines_of_code": analysis_result.average_nloc,
                "average_token_count": analysis_result.average_token_count,
                "average_cyclomatic_complexity": analysis_result.average_cyclomatic_complexity,
                "average_parameter_count": analysis_result.functions_average(
                    "parameter_count"
                ),
            }
