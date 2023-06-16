import pytest

from fregepoc.analyzers.tests.generic.ruby.constans import MOCKED_RUBY_FILES
from fregepoc.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from fregepoc.repositories.constants import ProgrammingLanguages

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
            ##sniper tests
            (
                {"repo_relative_file_path": "Sniper-Game/sniper.rb"},
                12.4,
                0.2,
            ),
            #####
            
            (
                {"repo_relative_file_path": "data_mapper.rb"},
                4.5,
                0.0,
            ),
            (
                {"repo_relative_file_path": "file_read.rb"},
                0.0,
                0.0,
            ),
            (
                {"repo_relative_file_path": "expand_path.rb"},
                0.0,
                0.0,
            ),
            (
                {"repo_relative_file_path": "EmptyFile.rb"},
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
            MOCKED_RUBY_FILES,
            ProgrammingLanguages.RUBY,
            tested_parameter_types,
        )
