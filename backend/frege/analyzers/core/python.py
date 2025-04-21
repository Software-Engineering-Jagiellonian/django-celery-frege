from typing import TypedDict

from radon.metrics import h_visit, mi_rank, mi_visit
from radon.raw import analyze

from frege.analyzers.core.base import AnalyzerFactory, BaseAnalyzer
from frege.repositories.constants import ProgrammingLanguages
from frege.repositories.utils.analyzers import repo_file_content


class PythonFileAnalysisResult(TypedDict):
    """
    A dictionary of metrics resulting from analyzing a Python file.

    Attributes:
        halstead_metrics (list[list[float]]): Halstead complexity metrics.
        LOC_metrics (list[int]): Lines of Code (LOC) metrics.
        MIM_rank_metrics (str): Maintainability Index rank (e.g., A, B, C).
        MIM_visit_metrics (float): Raw Maintainability Index score.
    """
    halstead_metrics: list[list[float]]
    LOC_metrics: list[int]
    MIM_rank_metrics: str
    MIM_visit_metrics: float


@AnalyzerFactory.register(ProgrammingLanguages.PYTHON)
class PythonAnalyzer(BaseAnalyzer[PythonFileAnalysisResult]):
    """
    Analyzer for Python source files.

    Uses Radon to compute code metrics such as Halstead complexity, 
    lines of code, and maintainability index.
    """
    def analyze(self, repo_file_obj):
        """
        Analyze the given Python repository file and extract metrics.

        Args:
            repo_file_obj (RepositoryFile): The repository file to analyze.

        Returns:
            PythonFileAnalysisResult: A dictionary containing metrics extracted 
            using Radon, including Halstead complexity, LOC, and maintainability.
        """
        with repo_file_content(repo_file_obj) as file_content:
            return {
                "halstead_metrics": h_visit(file_content),
                "LOC_metrics": analyze(file_content),
                "MIM_visit_metrics": (score := mi_visit(file_content, True)),
                "MIM_rank_metrics": mi_rank(score),
            }
