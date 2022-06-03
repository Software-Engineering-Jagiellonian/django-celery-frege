import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.csharp.constants import MOCKED_CSHARP_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestCSharpAverageCyclomaticComplexity:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_cyc"],
        [
            (
                {"repo_relative_file_path": "BinarySearchTree.cs"},
                2.636,
            ),
            (
                {"repo_relative_file_path": "QuickSort.cs"},
                7.0,
            )
        ],
    )
    def test_count_loc(
        self, repo_file_params, expected_cyc, settings, dummy_repo
    ):
        settings.DOWNLOAD_PATH = MOCKED_CSHARP_FILES
        analyzers = AnalyzerFactory.make_analyzers(ProgrammingLanguages.C_SHARP)
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.C_SHARP,
            **repo_file_params,
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["average_cyclomatic_complexity"] == pytest.approx(
                expected_cyc, 0.01
            )
