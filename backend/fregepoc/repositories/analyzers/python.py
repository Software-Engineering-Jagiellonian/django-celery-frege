from typing import TypedDict

from radon.metrics import h_visit, mi_rank, mi_visit
from radon.raw import analyze

from fregepoc.repositories.analyzers.base import BaseAnalyzer


class PythonFileAnalysisResult(TypedDict):
    halstead_metrics: list[list[float]]
    LOC_metrics: list[int]
    MIM_rank_metrics: str
    MIM_visit_metrics: float


class PythonAnalyzer(BaseAnalyzer[[str], PythonFileAnalysisResult]):
    @classmethod
    def analyze(cls, file_content):
        return {
            "halstead_metrics": h_visit(file_content),
            "LOC_metrics": analyze(file_content),
            "MIM_visit_metrics": (score := mi_visit(file_content, True)),
            "MIM_rank_metrics": mi_rank(score),
        }
