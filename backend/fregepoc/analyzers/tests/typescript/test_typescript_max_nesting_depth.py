import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.typescript.constants import (
    MOCKED_TYPESCRIPT_FILES,
)
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestTypescriptAnalyzerMaxNestingDepth:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_max_nesting_depth"],
        [
            (
                {"repo_relative_file_path": "bst.ts"},
                4,
            ),
            (
                {"repo_relative_file_path": "empty.ts"},
                0,
            ),
            (
                {"repo_relative_file_path": "bubble_sort.ts"},
                4,
            ),
            (
                {"repo_relative_file_path": "fast_fibbonaci.ts"},
                2,
            ),
        ],
    )
    def test_count_loc(
        self,
        repo_file_params,
        expected_max_nesting_depth,
        settings,
        dummy_repo,
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
            assert actual["max_nesting_depth"] == expected_max_nesting_depth
