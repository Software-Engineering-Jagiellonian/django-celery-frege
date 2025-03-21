import pytest

from frege.analyzers.tests.generic.golang.constants import (
    MOCKED_GOLANG_FILES,
)
from frege.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from frege.repositories.constants import ProgrammingLanguages
from frege.analyzers.tests.generic.util.mock_lizard_result import mock_lizard_result

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
                2,
                1671,
            )
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
            mock_lizard_result(
                average_cyclomatic_complexity=expected_average_cyc,
                average_nloc=expected_average_loc,
                average_parameter_count=expected_average_param_count,
                average_token_count=expected_average_token_count,
                nloc=expected_loc,
                token_count=expected_token_count
                ),
        )
