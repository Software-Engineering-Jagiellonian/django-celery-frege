import pytest

from frege.analyzers.tests.generic.ruby.constans import MOCKED_RUBY_FILES
from frege.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from frege.repositories.constants import ProgrammingLanguages
from frege.analyzers.tests.generic.util.mock_lizard_result import mock_lizard_result

tested_parameter_types = ["average_lines_of_code", "average_parameter_count"]


@pytest.mark.django_db
class TestRubyAnalyzer:
    @pytest.mark.parametrize(
        [
            "repo_file_params",
            "expected_average_loc",
            "expected_average_parameter_count",
        ],
        [
            (
                {"repo_relative_file_path": "data_mapper.rb"},
                4.5,
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
            MOCKED_RUBY_FILES,
            ProgrammingLanguages.RUBY,
            tested_parameter_types,
            mock_lizard_result(average_nloc=expected_average_loc, average_parameter_count=expected_average_parameter_count),
        )
