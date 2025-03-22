import pytest

from frege.analyzers.tests.generic.rust.constants import MOCKED_RUST_FILES
from frege.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from frege.repositories.constants import ProgrammingLanguages

tested_parameter_types = [
    "average_lines_of_code",
    "average_cyclomatic_complexity",
    "average_lines_of_code",
    "average_parameter_count",
    "token_count",
]


@pytest.mark.django_db
class TestRustAnalyzer:
    @pytest.mark.parametrize(
        [
            "repo_file_params",
            "expected_average_loc",
            "expected_cyc",
            "expected_average_lines_of_code",
            "expected_average_parameter_count",
            "expected_token_count",
        ],
        [
            (
                {"repo_relative_file_path": "iban.rs"},
                32.0,
                5.0,
                32.0,
                0.5,
                690,
            ),
            (
                {"repo_relative_file_path": "perlin_noise.rs"},
                8.20,
                2.2,
                8.2,
                2.2,
                1616,
            ),
            (
                {"repo_relative_file_path": "radix_search.rs"},
                6.33,
                2.0,
                6.33,
                1.33,
                240,
            ),
            (
                {"repo_relative_file_path": "empty.rs"},
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
        expected_average_loc,
        expected_cyc,
        expected_average_lines_of_code,
        expected_average_parameter_count,
        expected_token_count,
    ):
        expected = [
            expected_average_loc,
            expected_cyc,
            expected_average_lines_of_code,
            expected_average_parameter_count,
            expected_token_count,
        ]

        generic_test(
            repo_file_params,
            expected,
            settings,
            dummy_repo,
            MOCKED_RUST_FILES,
            ProgrammingLanguages.RUST,
            tested_parameter_types,
        )
