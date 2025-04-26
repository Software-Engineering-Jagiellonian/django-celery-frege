import pytest
from frege.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from frege.repositories.constants import ProgrammingLanguages
from frege.analyzers.tests.generic.util.mock_lizard_result import mock_lizard_result

tested_parameter_types = [
    "average_cyclomatic_complexity",
    "average_function_name_length",
    "average_lines_of_code",
    "average_token_count",
    "function_count",
    "lines_of_code",
    "token_count",
]


@pytest.mark.django_db
class TestScalaAnalyzer:
    @pytest.mark.parametrize(
        [
            "repo_file_params",
            "expected_cyc",
            "expected_average_function_name_length",
            "expected_average_loc",
            "expected_avg_token_count",
            "expected_function_count",
            "expected_loc",
            "expected_token_count",
        ],
        [
            (
                {"repo_relative_file_path": "BinaryTree.scala"},
                1.75,
                5,
                5.0,
                34.1,
                2,
                44,
                341,
            ),
        ],
    )
    def test(
        self,
        repo_file_params,
        dummy_repo,
        expected_cyc,
        expected_average_function_name_length,
        expected_average_loc,
        expected_avg_token_count,
        expected_function_count,
        expected_loc,
        expected_token_count,
    ):
        expected = [
            expected_cyc,
            expected_average_function_name_length,
            expected_average_loc,
            expected_avg_token_count,
            expected_function_count,
            expected_loc,
            expected_token_count,
        ]

        generic_test(
            repo_file_params,
            expected,
            dummy_repo,
            ProgrammingLanguages.SCALA,
            tested_parameter_types,
            mock_lizard_result(
                average_cyclomatic_complexity=expected_cyc,
                average_nloc=expected_average_loc,
                average_token_count=expected_avg_token_count,
                nloc=expected_loc,
                token_count=expected_token_count,
            ),
        )
