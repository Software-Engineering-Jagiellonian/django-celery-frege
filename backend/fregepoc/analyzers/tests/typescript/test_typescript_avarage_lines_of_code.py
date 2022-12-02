import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.typescript.constants import (
    MOCKED_TYPESCRIPT_FILES,
)
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestTypescriptAnalyzerAvarageLinesOfCode:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_avarage_loc"],
        [
            (
                {"repo_relative_file_path": "bst.ts"},
                8,
            ),
            (
                {"repo_relative_file_path": "empty.ts"},
                0,
            ),
        ],
    )
    def test_count_loc(
        self, repo_file_params, expected_avarage_loc, settings, dummy_repo
    ):
        settings.DOWNLOAD_PATH = MOCKED_TYPESCRIPT_FILES
        analyzers = AnalyzerFactory.make_analyzers(
            ProgrammingLanguages.TYPESCRIPT
        )
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.TYPESCRIPT,
            **repo_file_params,
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["average_lines_of_code"] == expected_avarage_loc
