from typing import TypedDict

from radon.metrics import h_visit, mi_rank, mi_visit
from radon.raw import analyze

from frege.analyzers.core.base import AnalyzerFactory, BaseAnalyzer
from frege.repositories.constants import ProgrammingLanguages
from frege.repositories.utils.analyzers import repo_file_content


class PythonFileAnalysisResult(TypedDict):
    halstead_metrics: list[list[float]]
    LOC_metrics: list[int]
    MIM_rank_metrics: str
    MIM_visit_metrics: float


@AnalyzerFactory.register(ProgrammingLanguages.PYTHON)
class PythonAnalyzer(BaseAnalyzer[PythonFileAnalysisResult]):
    def analyze(self, repo_file_obj):
        with repo_file_content(repo_file_obj) as file_content:
            return {
                "halstead_metrics": h_visit(file_content),
                "LOC_metrics": analyze(file_content),
                "MIM_visit_metrics": (score := mi_visit(file_content, True)),
                "MIM_rank_metrics": mi_rank(score),
            }
