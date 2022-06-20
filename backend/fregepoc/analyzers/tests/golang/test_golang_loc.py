import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.golang.constants import MOCKED_GOLANG_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestGolangAnalyzerLinesOfCode:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_loc"],
        [
            (
                {"repo_relative_file_path": "binary_tree.go"},
                297,
            ),
            (
                {"repo_relative_file_path": "concurrent_prime_sieve.go"},
                26,
            ),
            (
                {"repo_relative_file_path": "http_server.go"},
                31,
            ),
            (
                {"repo_relative_file_path": "tree_comparison.go"},
                65,
            ),
        ],
    )
    def test_count_loc(
        self, repo_file_params, expected_loc, settings, dummy_repo
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
            assert actual["lines_of_code"] == pytest.approx(
                expected_loc, 0.01
            )
