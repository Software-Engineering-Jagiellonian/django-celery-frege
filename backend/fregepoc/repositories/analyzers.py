from radon.metrics import h_visit, mi_visit, mi_rank
from radon.raw import analyze

# NOTE: this file is meant to be split into a folder with files representing analyzers


class BaseAnalyzer:
    @classmethod
    def analyze(file_path):
        raise NotImplementedError


class PythonAnalyzer(BaseAnalyzer):
    @classmethod
    def analyze(file_path, file_content):
        score = mi_visit(file_content, True)

        return {
            'halstead_metrics': h_visit(file_content),
            'LOC_metrics': analyze(file_content),
            'MIM_visit_metrics': score,
            'MIM_rank_metrics': mi_rank(score)
        }
