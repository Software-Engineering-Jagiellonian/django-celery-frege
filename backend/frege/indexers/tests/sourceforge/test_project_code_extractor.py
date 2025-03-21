import pytest
import requests
from bs4 import BeautifulSoup
from pytest_mock import MockerFixture

from frege.indexers.sourceforge.project_code_extractor import (
    GitCloneInfo,
    SourceforgeProjectCodeExtractor,
    extract_clone_url,
    extract_commit,
)
from frege.indexers.tests.sourceforge import MOCKED_SOURCEFORGE_FILES


@pytest.fixture
def soup():
    with open(
        MOCKED_SOURCEFORGE_FILES / "sourceforge_project_code_page.html",
        encoding="utf8",
    ) as f:
        page = f.read()
    return BeautifulSoup(page, features="html.parser")


@pytest.fixture
def mocked_sourceforge_response():
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
    def test_extract_commit(self, soup):
        commit_hash = extract_commit(soup)
        expected_commit = "53fba0e052502d7192bacdcef1bd8a51b066686b"
        assert commit_hash == expected_commit, f"Expected {expected_commit}, got {commit_hash}"

    def test_extract_clone_url(self, soup):
        git_clone_info = extract_clone_url(soup)
        expected_info = GitCloneInfo(
            url="https://git.code.sf.net/p/mingw/build-aux",
            commit_hash="53fba0e052502d7192bacdcef1bd8a51b066686b",
        )
        assert git_clone_info == expected_info, f"Expected {expected_info}, got {git_clone_info}"

    def test_extract(self, mocker: MockerFixture, mocked_sourceforge_response):
        mock_requests_get = mocker.patch("requests.get", side_effect=mocked_sourceforge_response)

        code_url = "test_string"
        git_clone_info = SourceforgeProjectCodeExtractor().extract(code_url=code_url)

        mock_requests_get.assert_called_once_with(f"https://sourceforge.net/{code_url}")
        assert git_clone_info is None, "Expected None for the mocked SourceForge response"
