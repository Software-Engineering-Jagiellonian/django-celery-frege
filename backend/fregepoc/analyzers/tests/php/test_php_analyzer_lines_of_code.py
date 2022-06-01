import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.php.constans import MOCKED_PHP_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestPhpAnalyzerLinesOfCode:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_average_loc"],
        [
            (
                {"repo_relative_file_path": "main.php"},
                1.71,
            ),
            (
                {"repo_relative_file_path": "User.php"},
                4.61,
            ),
            (
                {"repo_relative_file_path": "UserController.php"},
                5.0,
            ),
        ],
    )
    def test_count_loc(
        self, repo_file_params, expected_average_loc, settings, dummy_repo
    ):
        settings.DOWNLOAD_PATH = MOCKED_PHP_FILES
        analyzers = AnalyzerFactory.make_analyzers(ProgrammingLanguages.PHP)
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.PHP,
            **repo_file_params,
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["average_lines_of_code"] == pytest.approx(
                expected_average_loc, 0.01
            )