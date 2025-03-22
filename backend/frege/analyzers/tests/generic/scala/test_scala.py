import pytest

from frege.analyzers.tests.generic.scala.constants import MOCKED_SCALA_FILES
from frege.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from frege.repositories.constants import ProgrammingLanguages

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
                6.75,
                5.0,
                34.1,
                8,
                44,
                341,
            ),
            (
                {"repo_relative_file_path": "InsertionSort.scala"},
                2.0,
                4.66,
                8.0,
                83.0,
                3,
                23,
                250,
            ),
            (
                {"repo_relative_file_path": "PrimeNumbers.scala"},
                1.0,
                7.5,
                4.0,
                30.5,
                2,
                8,
                63,
            ),
            (
                {"repo_relative_file_path": "EmptyFile.scala"},
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
            settings,
            dummy_repo,
            MOCKED_SCALA_FILES,
            ProgrammingLanguages.SCALA,
            tested_parameter_types,
        )
