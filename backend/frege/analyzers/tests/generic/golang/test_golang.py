import pytest

from frege.analyzers.tests.generic.golang.constants import (
    MOCKED_GOLANG_FILES,
)
from frege.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from frege.repositories.constants import ProgrammingLanguages

tested_parameter_types = [
    "average_cyclomatic_complexity",
    "average_lines_of_code",
    "average_parameter_count",
    "average_token_count",
    "lines_of_code",
    "function_count",
    "token_count",
]


@pytest.mark.django_db
class TestGolangAnalyzer:
    @pytest.mark.parametrize(
        [
            "repo_file_params",
            "expected_average_cyc",
            "expected_average_loc",
            "expected_average_param_count",
            "expected_average_token_count",
            "expected_loc",
            "expected_no_functions",
            "expected_token_count",
        ],
        [
            (
                {"repo_relative_file_path": "binary_tree.go"},
                2.92,
                11.67,
                1.13,
                67.88,
                297,
                24,
                1671,
            ),
            (
                {"repo_relative_file_path": "concurrent_prime_sieve.go"},
                2.34,
                8.0,
                1.33,
                42.0,
                26,
                3,
                130,
            ),
            (
                {"repo_relative_file_path": "http_server.go"},
                2.0,
                8.0,
                0,
                50.67,
                31,
                3,
                161,
            ),
            (
                {"repo_relative_file_path": "tree_comparison.go"},
                2.14,
                8.0,
                1.29,
                49.14,
                65,
                7,
                363,
            ),
            (
                {"repo_relative_file_path": "EmptyFile.go"},
                0,
                0,
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
        expected_average_cyc,
        expected_average_loc,
        expected_average_param_count,
        expected_average_token_count,
        expected_loc,
        expected_no_functions,
        expected_token_count,
    ):
        expected = [
            expected_average_cyc,
            expected_average_loc,
            expected_average_param_count,
            expected_average_token_count,
            expected_loc,
            expected_no_functions,
            expected_token_count,
        ]

        generic_test(
            repo_file_params,
            expected,
            settings,
            dummy_repo,
            MOCKED_GOLANG_FILES,
            ProgrammingLanguages.GOLANG,
            tested_parameter_types,
        )
