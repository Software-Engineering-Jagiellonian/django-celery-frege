import pytest

from fregepoc.analyzers.tests.generic.typescript.constants import (
    MOCKED_TYPESCRIPT_FILES,
)
from fregepoc.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from fregepoc.repositories.constants import ProgrammingLanguages

tested_parameter_types = [
    "average_cyclomatic_complexity",
    "average_lines_of_code",
    "average_token_count",
    "lines_of_code",
    "token_count",
]


@pytest.mark.django_db
class TestTypescriptAnalyzer:
    @pytest.mark.parametrize(
        [
            "repo_file_params",
            "expected_avg_cyclomatic_complexity",
            "expected_average_loc",
            "expected_avg_token_count",
            "expected_loc",
            "expected_token_count",
        ],
        [
            ##Nest-ReactTS-Minigame test
                (
                {"repo_relative_file_path": "Nest-ReactTS-Minigame/mini-battle-backend/src/main.ts"},
                2,
                7,
                39.5,
                20,
                125,
            ),

            ###




            (
                {"repo_relative_file_path": "bst.ts"},
                1.0,
                3.0,
                13.0,
                45,
                305,
            ),
            (
                {"repo_relative_file_path": "bubble_sort.ts"},
                2.0,
                5.66,
                49.0,
                22,
                205,
            ),
            (
                {"repo_relative_file_path": "fast_fibbonaci.ts"},
                2.5,
                10.0,
                51.0,
                25,
                167,
            ),
            (
                {"repo_relative_file_path": "empty.ts"},
                0,
                0,
                0,
                0,
                0,
            ),
        ],
    )
    def test(
        self,
        repo_file_params,
        settings,
        dummy_repo,
        expected_avg_cyclomatic_complexity,
        expected_average_loc,
        expected_avg_token_count,
        expected_loc,
        expected_token_count,
    ):
        expected = [
            expected_avg_cyclomatic_complexity,
            expected_average_loc,
            expected_avg_token_count,
            expected_loc,
            expected_token_count,
        ]

        generic_test(
            repo_file_params,
            expected,
            settings,
            dummy_repo,
            MOCKED_TYPESCRIPT_FILES,
            ProgrammingLanguages.TYPESCRIPT,
            tested_parameter_types,
        )
