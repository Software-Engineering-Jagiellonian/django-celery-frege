import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.golang.constants import MOCKED_GOLANG_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestGolangAnalyzerLinesOfCode:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_average_param_count"],
        [
            (
                {"repo_relative_file_path": "binary_tree.go"},
                1.13,
            ),
            (
                {"repo_relative_file_path": "concurrent_prime_sieve.go"},
                1.33,
            ),
            (
                {"repo_relative_file_path": "http_server.go"},
                0,
            ),
            (
                {"repo_relative_file_path": "tree_comparison.go"},
                1.29,
            ),
        ],
    )
    def test_average_param_count(
        self,
        repo_file_params,
        expected_average_param_count,
        settings,
        dummy_repo,
    ):
        settings.DOWNLOAD_PATH = MOCKED_GOLANG_FILES
        analyzers = AnalyzerFactory.make_analyzers(ProgrammingLanguages.GOLANG)
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.GOLANG,
            **repo_file_params,
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["average_parameter_count"] == pytest.approx(
                expected_average_param_count, 0.01
            )
