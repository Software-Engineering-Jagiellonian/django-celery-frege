from typing import TypedDict

import lizard

from frege.analyzers.core.base import BaseAnalyzer
from frege.repositories.utils.analyzers import (
    average_func_name_len,
    repo_file_content,
)
from frege.repositories.utils.paths import get_file_abs_path


class GenericAnalysisResult(TypedDict):
    """
    A dictionary that holds the results of analyzing a source code file.

    This dictionary contains various metrics calculated from the analysis, 
    such as lines of code, token count, average cyclomatic complexity, and 
    other function-related statistics.

    Keys:
        lines_of_code (int): The total number of lines of code in the file.
        token_count (int): The total number of tokens in the file.
        average_lines_of_code (float): The average number of lines of code per function.
        average_token_count (float): The average number of tokens per function.
        average_cyclomatic_complexity (float): The average cyclomatic complexity per function.
        average_parameter_count (float): The average number of parameters per function.
        function_count (int): The number of functions in the file.
        average_function_name_length (float): The average length of function names in the file.
    """
    lines_of_code: int
    token_count: int
    average_lines_of_code: float
    average_token_count: float
    average_cyclomatic_complexity: float
    average_parameter_count: float
    function_count: int
    average_function_name_length: float


def get_analysis_results(res):
    """
    Extracts and returns a dictionary of key metrics from a Lizard analysis result.

    This function processes the results of the Lizard analysis, which includes 
    information such as lines of code, function count, token count, cyclomatic 
    complexity, and other function-related statistics.

    Args:
        res (LizardAnalysisResult): The result object returned by Lizard's 
        analysis, containing various code metrics.

    Returns:
        dict: A dictionary containing the extracted metrics:
            - lines_of_code
            - token_count
            - function_count
            - average_function_name_length
            - average_lines_of_code
            - average_token_count
            - average_cyclomatic_complexity
            - average_parameter_count
    """
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
    """
    Analyzes a source code file using the Lizard library to gather metrics about 
    the code's structure, including lines of code, token count, function count, 
    and cyclomatic complexity.

    This class implements the `analyze()` method defined in the BaseAnalyzer, 
    using Lizard's analysis results to compute various metrics related to the 
    source code file.

    Methods:
        analyze(repo_file_obj): Analyzes the given repository file and returns 
        a dictionary with key metrics (lines of code, token count, average function 
        name length, etc.) calculated using the Lizard analysis.
    """
    
    def analyze(self, repo_file_obj):
        """
        Analyzes the given repository file and returns key metrics on its structure.

        This method reads the source code of the given repository file, analyzes 
        it using the Lizard library, and then returns a dictionary containing 
        key metrics, such as lines of code, token count, function count, and 
        other relevant statistics.

        Args:
            repo_file_obj (RepositoryFile): The repository file object to analyze.

        Returns:
            GenericAnalysisResult: A dictionary containing the analysis results, 
            including lines of code, token count, function count, and other key 
            metrics.
        """

        with repo_file_content(repo_file_obj) as source_code:
            analysis_result = lizard.analyze_file.analyze_source_code(
                str(get_file_abs_path(repo_file_obj)), source_code
            )
            return get_analysis_results(analysis_result)
