import pytest

from fregepoc.analyzers.tests.generic.java.constants import MOCKED_JAVA_FILES
from fregepoc.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from fregepoc.repositories.constants import ProgrammingLanguages

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
        
            #tests for calculator
            (
                {"repo_relative_file_path": "Calculator/src/main/java/com/houarizegai/calculator/App.java"},
                1.0,
                3.0,
                1.0,
                14.0,
                7,
                40,
            ),

            ######

            (
                {"repo_relative_file_path": "BinaryTree.java"},
                1.77,
                7.31,
                0.73,
                48.23,
                240,
                1553,
            ),
            (
                {"repo_relative_file_path": "ImmutableListMultimap.java"},
                1.55,
                6.26,
                1.87,
                48.74,
                261,
                2151,
            ),
            (
                {"repo_relative_file_path": "TypeToken.java"},
                2.55,
                8.15,
                1.15,
                59.25,
                182,
                1388,
            ),
            (
                {"repo_relative_file_path": "EmptyFile.java"},
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
        )
