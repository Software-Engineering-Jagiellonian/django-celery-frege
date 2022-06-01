import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.javascript.constants import MOCKED_JAVASCRIPT_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestJavascriptAnalyzerLinesOfCode:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_loc"],
        [
            (
                {"repo_relative_file_path": "insertionSort.js"},
                460,
            ),
            (
                {"repo_relative_file_path": "palindrome.js"},
                460,
            ),
            (
                {"repo_relative_file_path": "stringSimilarity.js"},
                460,
            ),
            (
                {"repo_relative_file_path": "maximumSubarraySum.js"},
                460,
            ),
            (
                {"repo_relative_file_path": "dijkstra.js"},
                460,
            ),
        ],
    )
    def test_count_loc(
        self, repo_file_params, expected_loc, settings, dummy_repo
    ):
        settings.DOWNLOAD_PATH = MOCKED_JAVASCRIPT_FILES
        analyzers = AnalyzerFactory.make_analyzers(ProgrammingLanguages.JS)
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.JS,
            **repo_file_params,
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["lines_of_code"] == expected_loc
