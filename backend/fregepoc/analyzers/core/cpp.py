import contextlib
from typing import TypedDict

import lizard
from lizard import analyze_file

from fregepoc.analyzers.core.base import AnalyzerFactory, BaseAnalyzer
from fregepoc.analyzers.core.exceptions import LizardException
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.utils.analyzers import repo_file_content
from fregepoc.repositories.utils.paths import get_file_abs_path


class AnalyzeResult:
    def __init__(self, result):
        self.filename = result["filename"]
        self.nloc = result["nloc"]
        self.function_list = result["function_list"] or []
        self.token_count = result["token_count"]

    average_lines_of_code = property(
        lambda self: self.functions_average("nloc")
    )
    average_token_count = property(
        lambda self: self.functions_average("token_count")
    )
    average_cyclomatic_complexity = property(
        lambda self: self.functions_average("cyclomatic_complexity")
    )
    average_parameter_count = property(
        lambda self: self.functions_average("parameter_count")
    )
    average_nesting_depth = property(
        lambda self: self.functions_average("max_nesting_depth")
    )
    max_nesting_depth = property(
        lambda self: max(fun.max_nesting_depth for fun in self.function_list)
    )

    def functions_average(self, att):
        summary = sum(getattr(fun, att) for fun in self.function_list)
        return summary / len(self.function_list) if self.function_list else 0

    def as_dict(self):
        return {
            "lines_of_code": int(self.nloc),
            "token_count": int(self.token_count),
            "average_lines_of_code": int(self.average_lines_of_code),
            "average_token_count": int(self.average_token_count),
            "average_cyclomatic_complexity": int(
                self.average_cyclomatic_complexity
            ),
            "average_parameter_count": int(self.average_parameter_count),
            "average_nesting_depth": int(self.average_nesting_depth),
            "max_nesting_depth": int(self.max_nesting_depth),
        }


class CppFileAnalysisResult(TypedDict):
    lines_of_code: int
    token_count: int
    average_lines_of_code: int
    average_token_count: int
    average_cyclomatic_complexity: int
    average_parameter_count: int
    average_nesting_depth: int
    max_nesting_depth: int


@AnalyzerFactory.register(ProgrammingLanguages.CPP)
class CppAnalyzer(BaseAnalyzer[CppFileAnalysisResult]):
    def analyze(self, repo_file_obj):
        with contextlib.suppress(LizardException):
            lizard.get_extensions(["nd"])
            with repo_file_content(repo_file_obj) as source_code:
                return AnalyzeResult(vars(analyze_file.analyze_source_code(
                    str(get_file_abs_path(repo_file_obj)), source_code
                ))).as_dict()
