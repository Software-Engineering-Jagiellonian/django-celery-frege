import json
from pathlib import Path

import pytest
import requests
from pytest_mock import MockerFixture

from frege.indexers.models import BitbucketIndexer
from frege.indexers.tests.constants import MOCK_DIR


def mocked_requests_get(repositories, forks, commits):
    """
    Returns a mock implementation of `requests.get` that provides
    predefined responses for Bitbucket API endpoints based on the
    requested URL suffix.

    Args:
        repositories (tuple): (filename, status_code) for /repositories
        forks (tuple): (filename, status_code) for /forks
        commits (tuple): (filename, status_code) for /commits

    Returns:
        callable: a function to be used as `side_effect` in mocking `requests.get`
    """
    class MockResponse:
        def __init__(self, response_file, status_code):
            response_text = Path(
                MOCK_DIR / f"{response_file}.json"
            ).read_text()
            self.json_data = json.loads(response_text)
            self.status_code = status_code

        def json(self):
            return self.json_data

        def __bool__(self):
            return self.status_code < 400

    def inner_mock(*args, **kwargs):
        if args[0].endswith("/repositories"):
            return MockResponse(*repositories)
        elif args[0].endswith("/forks"):
            return MockResponse(*forks)
        elif args[0].endswith("/commits"):
            return MockResponse(*commits)
        else:
            return MockResponse(None, 404)

    return inner_mock


class TestBitbucketIndexer:
    """
    Integration tests for the BitbucketIndexer model, simulating
    interaction with the Bitbucket API via mocked HTTP responses.
    """

    @pytest.mark.django_db
    def test_bitbucket(self, mocker: MockerFixture) -> None:
        """
        Tests the successful indexing of a Bitbucket repository by mocking
        /repositories, /forks, and /commits endpoints. Verifies that the
        BitbucketIndexer yields a correctly parsed repository object.
        """
        mocker.patch("frege.indexers.models.BitbucketIndexer.save")
        mocker.patch(
            "requests.get",
            side_effect=mocked_requests_get(
                repositories=("bitbucket_repo", 200),
                forks=("bitbucket_forks", 200),
                commits=("bitbucket_commits", 200),
            ),
        )

        repos_to_process = next(iter(BitbucketIndexer()))

        assert len(repos_to_process) == 1
        assert requests.get.call_count == 3

        repo = repos_to_process.pop()

        assert repo.name == "git-scripts"
        assert repo.description == ""
        assert repo.git_url == "https://bitbucket.org/jwalton/git-scripts.git"
        assert repo.repo_url == "https://bitbucket.org/jwalton/git-scripts"
        assert repo.commit_hash == "b1129dedc99ed09faf74ef3c0a88e55685c637b2"

    @pytest.mark.django_db
    def test_bitbucket_on_error(self, mocker: MockerFixture) -> None:
        """
        Tests the behavior of BitbucketIndexer when the initial API call
        to /repositories fails (e.g., rate limited with 429 status code).
        Verifies that iteration raises StopIteration and no further calls are made.
        """
        mocker.patch(
            "requests.get",
            side_effect=mocked_requests_get(
                repositories=("bitbucket_error", 429), forks=None, commits=None
            ),
        )

        with pytest.raises(StopIteration):
            next(iter(BitbucketIndexer()))

        assert requests.get.call_count == 1
