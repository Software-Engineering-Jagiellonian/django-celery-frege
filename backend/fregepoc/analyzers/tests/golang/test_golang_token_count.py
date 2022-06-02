import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.golang.constants import MOCKED_GOLANG_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestGolangAnalyzerLinesOfCode:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_token_count"],
        [
            (
                {"repo_relative_file_path": "binary_tree.go"},
                1671,
            ),
            (
                {"repo_relative_file_path": "concurrent_prime_sieve.go"},
                130,
            ),
            (
                {"repo_relative_file_path": "http_server.go"},
                161,
            ),
            (
                {"repo_relative_file_path": "tree_comparison.go"},
                363,
            ),
        ],
    )
    def test_token_count(
        self, repo_file_params, expected_token_count, settings, dummy_repo
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
            assert actual["token_count"] == expected_token_count
