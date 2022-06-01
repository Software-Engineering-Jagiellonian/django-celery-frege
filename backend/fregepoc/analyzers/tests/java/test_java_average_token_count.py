import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.java.constants import MOCKED_JAVA_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestJavaAnalyzerLinesOfCode:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_average_token_count"],
        [
            (
                {"repo_relative_file_path": "BinaryTree.java"},
                48.23,
            ),
            (
                {"repo_relative_file_path": "ImmutableListMultimap.java"},
                48.74,
            ),
            (
                {"repo_relative_file_path": "TypeToken.java"},
                59.25,
            ),
        ],
    )
    def test_count_loc(
        self,
        repo_file_params,
        expected_average_token_count,
        settings,
        dummy_repo,
    ):
        settings.DOWNLOAD_PATH = MOCKED_JAVA_FILES
        analyzers = AnalyzerFactory.make_analyzers(ProgrammingLanguages.JAVA)
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.JAVA,
            **repo_file_params,
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["average_token_count"] == pytest.approx(
                expected_average_token_count, 0.01
            )
