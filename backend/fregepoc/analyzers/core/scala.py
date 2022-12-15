from typing import TypedDict

import lizard

from fregepoc.analyzers.core.base import AnalyzerFactory, BaseAnalyzer
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.utils.analyzers import repo_file_content


class ScalaFileAnalysisResult(TypedDict):
    lines_of_code: int
    token_count: int
    average_lines_of_code: float
    average_token_count: float
    average_cyclomatic_complexity: float
    function_count: int
    average_function_name_length: float
    average_parameter_count: float


@AnalyzerFactory.register(ProgrammingLanguages.SCALA)
class ScalaAnalyzer(BaseAnalyzer[ScalaFileAnalysisResult]):
    def analyze(self, repo_file_obj):
        with repo_file_content(repo_file_obj) as file_content:
            analysis_result = lizard.analyze_file.analyze_source_code(
                ".scala", file_content
            )

            def average_func_name_len(function_list):
                func_name_lengths = [len(func.name) for func in function_list]
                return sum(func_name_lengths) / len(func_name_lengths) if func_name_lengths else 0.0

            return {
                "lines_of_code": analysis_result.nloc,
                "token_count": analysis_result.token_count,
                "average_lines_of_code": analysis_result.average_nloc,
                "average_token_count": analysis_result.average_token_count,
                "average_cyclomatic_complexity": analysis_result.average_cyclomatic_complexity,
                "function_count": len(analysis_result.function_list),
                "average_function_name_length": average_func_name_len(analysis_result.function_list),
                "average_parameter_count": analysis_result.functions_average(
                    "parameter_count"
                ),
            }
