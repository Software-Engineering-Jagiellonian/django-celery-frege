import pytest

from fregepoc.analyzers.tests.generic.java.constants import MOCKED_JAVA_FILES
from fregepoc.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.analyzers.tests.generic.util.mock_lizard_result import mock_lizard_result

tested_parameter_types = [
    "average_cyclomatic_complexity",
    "average_lines_of_code",
    "average_parameter_count",
    "average_token_count",
    "lines_of_code",
    "token_count",
]


@pytest.mark.django_db
class TestJavaAnalyzer:
    @pytest.mark.parametrize(
        [
            "repo_file_params",
            "expected_cyc",
            "expected_average_loc",
            "expected_average_parameter_count",
            "expected_average_token_count",
            "expected_loc",
            "expected_token_count",
        ],
        [
            (
                {"repo_relative_file_path": "BinaryTree.java"},
                1.77,
                7.31,
                0.73,
                48.23,
                240,
                1553,
            ),
        ],
    )
    def test(
        self,
        repo_file_params,
        settings,
        dummy_repo,
        expected_cyc,
        expected_average_loc,
        expected_average_parameter_count,
        expected_average_token_count,
        expected_loc,
        expected_token_count,
    ):
        expected = [
            expected_cyc,
            expected_average_loc,
            expected_average_parameter_count,
            expected_average_token_count,
            expected_loc,
            expected_token_count,
        ]

        generic_test(
            repo_file_params,
            expected,
            settings,
            dummy_repo,
            MOCKED_JAVA_FILES,
            ProgrammingLanguages.JAVA,
            tested_parameter_types,
            mock_lizard_result(        
                average_cyclomatic_complexity=expected_cyc,
                average_nloc=expected_average_loc,
                average_parameter_count=expected_average_parameter_count,
                average_token_count=expected_average_token_count,
                nloc=expected_loc,
                token_count=expected_token_count
                ),
        )
