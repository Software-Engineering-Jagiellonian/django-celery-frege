import pytest
from frege.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from frege.repositories.constants import ProgrammingLanguages
from frege.analyzers.tests.generic.util.mock_lizard_result import mock_lizard_result

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
            (
                {"repo_relative_file_path": "bst.ts"},
                3.75,
                3.0,
                13.0,
                45,
                305,
            ),
        ],
    )
    def test(
        self,
        repo_file_params,
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
            dummy_repo,
            ProgrammingLanguages.TYPESCRIPT,
            tested_parameter_types,
            mock_lizard_result(
                average_cyclomatic_complexity=expected_avg_cyclomatic_complexity,
                average_nloc=expected_average_loc,
                average_token_count=expected_avg_token_count,
                nloc=expected_loc,
                token_count=expected_token_count,
            ),
        )
