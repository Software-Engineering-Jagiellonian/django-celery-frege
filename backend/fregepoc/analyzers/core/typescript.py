from typing import TypedDict

import lizard

from fregepoc.analyzers.core.base import AnalyzerFactory, BaseAnalyzer
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.utils.analyzers import repo_file_content


class TypescriptFileAnalysisResult(TypedDict):
    lines_of_code: int
    token_count: int
    average_lines_of_code: int
    average_token_count: int
    average_cyclomatic_complexity: int
    average_parameter_count: int
    average_nesting_depth: int
    max_nesting_depth: int


@AnalyzerFactory.register(ProgrammingLanguages.TYPESCRIPT)
class JavascriptAnalyzer(BaseAnalyzer[TypescriptFileAnalysisResult]):
    def analyze(self, repo_file_obj):
        with repo_file_content(repo_file_obj) as file_content:
            result = lizard.analyze_file.analyze_source_code(
                ".ts", file_content
            )

            return {
                "lines_of_code": result.nloc,
                "token_count": result.token_count,
                "average_lines_of_code": result.average_nloc,
                "average_token_count": result.average_token_count,
                "average_cyclomatic_complexity": result.average_cyclomatic_complexity,
                "average_parameter_count": result.functions_average(
                    "parameter_count"
                ),
                "average_nesting_depth": result.functions_average(
                    "max_nesting_depth"
                ),
                "max_nesting_depth": max(
                    fun.max_nesting_depth for fun in result.function_list
                ),
            }
