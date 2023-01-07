from typing import TypedDict

import lizard

from fregepoc.analyzers.core.base import BaseAnalyzer
from fregepoc.repositories.utils.analyzers import (
    average_func_name_len,
    repo_file_content,
)
from fregepoc.repositories.utils.paths import get_file_abs_path


class GenericAnalysisResult(TypedDict):
    lines_of_code: int
    token_count: int
    average_lines_of_code: float
    average_token_count: float
    average_cyclomatic_complexity: float
    average_parameter_count: float
    function_count: int
    average_function_name_length: float


def get_analysis_results(res):
    return {
        "lines_of_code": res.nloc,
        "token_count": res.token_count,
        "function_count": len(res.function_list),
        "average_function_name_length": average_func_name_len(
            res.function_list
        ),
        "average_lines_of_code": res.average_nloc,
        "average_token_count": res.average_token_count,
        "average_cyclomatic_complexity": res.average_cyclomatic_complexity,
        "average_parameter_count": res.functions_average("parameter_count"),
    }


class GenericAnalyzer(BaseAnalyzer[GenericAnalysisResult]):
    def analyze(self, repo_file_obj):
        with repo_file_content(repo_file_obj) as source_code:
            analysis_result = lizard.analyze_file.analyze_source_code(
                str(get_file_abs_path(repo_file_obj)), source_code
            )
            return get_analysis_results(analysis_result)
