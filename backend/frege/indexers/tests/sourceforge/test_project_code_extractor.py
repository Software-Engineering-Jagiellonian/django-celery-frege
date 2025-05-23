import pytest
import requests
from bs4 import BeautifulSoup
from pytest_mock import MockerFixture
from unittest.mock import patch

from frege.indexers.sourceforge.project_code_extractor import (
    GitCloneInfo,
    SourceforgeProjectCodeExtractor,
    extract_clone_url,
    extract_commit,
)
from frege.indexers.tests.sourceforge import MOCKED_SOURCEFORGE_FILES


@pytest.fixture
def soup():
    """
    Loads and returns a BeautifulSoup object from a static HTML page
    representing a SourceForge project code page, used for testing parsing logic.
    """
    with open(
        MOCKED_SOURCEFORGE_FILES / "sourceforge_project_code_page.html",
        encoding="utf8",
    ) as f:
        page = f.read()
    return BeautifulSoup(page, features="html.parser")


@pytest.fixture
def mocked_sourceforge_response():
    """
    Returns a mocked version of requests.get that reads and returns a
    pre-saved SourceForge HTML page for testing HTTP response handling.
    """
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code
            self.ok = (self.status_code == 200)

    def inner_mock(*args, **kwargs):
        with open(
            MOCKED_SOURCEFORGE_FILES / "sourceforge_project_code_page_2.html",
            encoding="utf8",
        ) as f:
            return MockResponse(f.read(), 200)

    return inner_mock


class TestSourceforgeProjectCodeExtractor:
    """
    Unit tests for the SourceforgeProjectCodeExtractor class and its helper functions.
    """

    def test_extract_commit(self, soup):
        """
        Tests whether the commit hash is correctly extracted from the sample HTML page.
        """
        commit_hash = extract_commit(soup)
        expected_commit = "53fba0e052502d7192bacdcef1bd8a51b066686b"
        assert commit_hash == expected_commit

    def test_extract_clone_url(self, soup):
        """
        Tests whether the clone URL and commit hash are correctly extracted
        from the SourceForge project code page.
        """
        git_clone_info = extract_clone_url(soup)
        expected_info = GitCloneInfo(
            url="https://git.code.sf.net/p/mingw/build-aux",
            commit_hash="53fba0e052502d7192bacdcef1bd8a51b066686b",
        )
        assert git_clone_info == expected_info

    def test_extract(self, mocker: MockerFixture, mocked_sourceforge_response):
        """
        Tests the extract() method with a mocked HTTP response. Ensures that None
        is returned when the page doesn't contain valid repository information.
        """
        mock_requests_get = mocker.patch("requests.get", side_effect=mocked_sourceforge_response)
        code_url = "test_string"
        git_clone_info = SourceforgeProjectCodeExtractor().extract(code_url=code_url)
        mock_requests_get.assert_called_once_with(f"https://sourceforge.net/{code_url}")
        assert git_clone_info is None


    def test_extract_commit_no_h2(self):
        soup = BeautifulSoup("<html><body><h1>No commit info</h1></body></html>", "html.parser")
        assert extract_commit(soup) is None

    def test_extract_commit_missing_link(self):
        soup = BeautifulSoup('<html><body><h2>Tree</h2></body></html>', "html.parser")
        assert extract_commit(soup) is None

    def test_extract_clone_url_no_input(self):
        soup = BeautifulSoup("<html><body><h2>Tree</h2></body></html>", "html.parser")
        assert extract_clone_url(soup) is None

    def test_extract_clone_url_bad_input_value(self):
        html = '<input id="access_url" value="not a clone command"/>'
        soup = BeautifulSoup(html, "html.parser")
        assert extract_clone_url(soup) is None

    def test_extract_http_failure(self, mocker: MockerFixture):
        mock_response = mocker.Mock()
        mock_response.ok = False
        mock_response.text = ""
        mocker.patch("requests.get", return_value=mock_response)

        result = SourceforgeProjectCodeExtractor.extract("invalid/path")
        assert result is None

    @patch('frege.indexers.sourceforge.project_code_extractor.extract_commit', return_value=None)
    def test_commit_hash_is_none(self, mock_extract_commit):
        html = '<input id="access_url" value="git clone https://example.com/repo.git">'
        soup = BeautifulSoup(html, 'html.parser')

        result = extract_clone_url(soup)

        assert result is None
