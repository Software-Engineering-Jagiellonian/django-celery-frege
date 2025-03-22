import pytest

from frege.analyzers.tests.generic.swift.constants import MOCKED_SWIFT_FILES
from frege.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from frege.repositories.constants import ProgrammingLanguages

tested_parameter_types = [
    "average_cyclomatic_complexity",
    "average_function_name_length",
    "average_lines_of_code",
    "average_parameter_count",
    "average_token_count",
    "function_count",
    "lines_of_code",
    "token_count",
]


@pytest.mark.django_db
class TestSwiftAnalyzer:
    @pytest.mark.parametrize(
        [
            "repo_file_params",
            "expected_cyc",
            "expected_average_function_name_length",
            "expected_average_loc",
            "expected_average_parameter_count",
            "expected_average_token_count",
            "expected_function_count",
            "expected_loc",
            "expected_token_count",
        ],
        [
            (
                {"repo_relative_file_path": "binary_search.swift"},
                4.0,
                12.0,
                14.0,
                3.0,
                130.0,
                1,
                16,
                185,
            ),
            (
                {"repo_relative_file_path": "bucket_sort.swift"},
                1.8,
                8.1,
                5.7,
                1.3,
                42.3,
                10,
                76,
                538,
            ),
            (
                {"repo_relative_file_path": "dijkstra.swift"},
                2.2,
                6.0,
                10.4,
                1.4,
                82.8,
                5,
                83,
                561,
            ),
            (
                {"repo_relative_file_path": "empty.swift"},
                0,
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
        expected_average_parameter_count,
        expected_average_token_count,
        expected_function_count,
        expected_loc,
        expected_token_count,
    ):
        expected = [
            expected_cyc,
            expected_average_function_name_length,
            expected_average_loc,
            expected_average_parameter_count,
            expected_average_token_count,
            expected_function_count,
            expected_loc,
            expected_token_count,
        ]

        generic_test(
            repo_file_params,
            expected,
            settings,
            dummy_repo,
            MOCKED_SWIFT_FILES,
            ProgrammingLanguages.SWIFT,
            tested_parameter_types,
        )
