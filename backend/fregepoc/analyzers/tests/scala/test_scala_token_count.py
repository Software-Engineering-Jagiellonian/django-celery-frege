import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.scala.constants import MOCKED_SCALA_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestScalaAnalyzerTokenCount:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_token_count"],
        [
            (
                {"repo_relative_file_path": "InsertionSort.scala"},
                250,
            ),
            (
                {"repo_relative_file_path": "EmptyFile.scala"},
                0,
            ),
            (
                {"repo_relative_file_path": "BinaryTree.scala"},
                341,
            ),
            (
                {"repo_relative_file_path": "PrimeNumbers.scala"},
                63,
            ),
        ],
    )
    def test_count_loc(
        self,
        repo_file_params,
        expected_token_count,
        settings,
        dummy_repo,
    ):
        settings.DOWNLOAD_PATH = MOCKED_SCALA_FILES
        analyzers = AnalyzerFactory.make_analyzers(
            ProgrammingLanguages.SCALA
        )
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.SCALA,
            **repo_file_params,
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["token_count"] == expected_token_count
