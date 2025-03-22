import pytest

from frege.analyzers.tests.generic.javascript.constants import (
    MOCKED_JAVASCRIPT_FILES,
)
from frege.analyzers.tests.generic.util.generic_test_util import (
    generic_test,
)
from frege.repositories.constants import ProgrammingLanguages

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
            (
                {"repo_relative_file_path": "palindrome.js"},
                190,
            ),
            (
                {"repo_relative_file_path": "stringSimilarity.js"},
                71,
            ),
            (
                {"repo_relative_file_path": "maximumSubarraySum.js"},
                39,
            ),
            (
                {"repo_relative_file_path": "dijkstra.js"},
                71,
            ),
        ],
    )
    def test(self, repo_file_params, settings, dummy_repo, expected_loc):
        expected = [expected_loc]

        generic_test(
            repo_file_params,
            expected,
            settings,
            dummy_repo,
            MOCKED_JAVASCRIPT_FILES,
            ProgrammingLanguages.JS,
            tested_parameter_types,
        )
