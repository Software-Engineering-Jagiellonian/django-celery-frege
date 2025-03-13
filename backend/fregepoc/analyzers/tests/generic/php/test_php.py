import pytest

from fregepoc.analyzers.tests.generic.php.constans import MOCKED_PHP_FILES
from fregepoc.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.analyzers.tests.generic.util.mock_lizard_result import mock_lizard_result

tested_parameter_types = ["average_lines_of_code", "average_parameter_count"]


@pytest.mark.django_db
class TestPhpAnalyzer:
    @pytest.mark.parametrize(
        [
            "repo_file_params",
            "expected_average_loc",
            "expected_average_parameter_count",
        ],
        [
            (
                {"repo_relative_file_path": "main.php"},
                1.71,
                0.0,
            ),
        ],
    )
    def test(
        self,
        repo_file_params,
        settings,
        dummy_repo,
        expected_average_loc,
        expected_average_parameter_count,
    ):
        expected = [expected_average_loc, expected_average_parameter_count]

        generic_test(
            repo_file_params,
            expected,
            settings,
            dummy_repo,
            MOCKED_PHP_FILES,
            ProgrammingLanguages.PHP,
            tested_parameter_types,
            mock_lizard_result(average_nloc=expected_average_loc, average_parameter_count=expected_average_parameter_count),
        )
