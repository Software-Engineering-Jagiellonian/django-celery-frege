import pytest

from fregepoc.analyzers.tests.generic.php.constans import MOCKED_PHP_FILES
from fregepoc.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from fregepoc.repositories.constants import ProgrammingLanguages

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
            ({"repo_relative_file_path": "User.php"}, 4.61, 0.84),
            (
                {"repo_relative_file_path": "UserController.php"},
                5.0,
                1.0,
            ),
            (
                {"repo_relative_file_path": "UserRepository.php"},
                4.75,
                1.0,
            ),
            (
                {"repo_relative_file_path": "EmptyFile.php"},
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
        )
