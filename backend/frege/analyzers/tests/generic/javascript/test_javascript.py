import pytest
from frege.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from frege.repositories.constants import ProgrammingLanguages
from frege.analyzers.tests.generic.util.mock_lizard_result import mock_lizard_result

tested_parameter_types = ["lines_of_code"]


@pytest.mark.django_db
class TestJavascriptAnalyzer:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_loc"],
        [
            (
                {"repo_relative_file_path": "insertionSort.js"},
                49,
            ),
        ],
    )
    def test(self, repo_file_params, dummy_repo, expected_loc):
        expected = [expected_loc]

        generic_test(
            repo_file_params,
            expected,
            dummy_repo,
            ProgrammingLanguages.JS,
            tested_parameter_types,
            mock_lizard_result(nloc=expected_loc),
        )
