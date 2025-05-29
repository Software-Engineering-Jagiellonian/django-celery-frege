from typing import Optional

import pytest
import requests
from bs4 import BeautifulSoup
from pytest_mock import MockerFixture

from frege.indexers.sourceforge.project_extractor import (
    SourceforgeProject,
    SourceforgeProjectExtractor,
)
from frege.indexers.sourceforge.projects_extractor import (
    SourceforgeProjectsExtractor,
    extract_projects_names,
)
from frege.indexers.tests.sourceforge.constants import MOCKED_SOURCEFORGE_FILES


@pytest.fixture(scope="module")
def soup():
    """
    Fixture that loads and returns a BeautifulSoup object from a static
    HTML file representing a SourceForge projects listing page.
    """
    with open(
        MOCKED_SOURCEFORGE_FILES / "sourceforge_projects_page.html",
        encoding="utf8",
    ) as f:
        page = f.read()
    return BeautifulSoup(page, features="html.parser")


@pytest.fixture(scope="module")
def expected_projects_names():
    """
    Fixture that provides a set of expected project names
    as found on the mocked SourceForge projects listing page.
    """
    return {
        "freepascal",
        "keylogger.mirror",
        "dispcalgui",
        "hf-auto-clicker",
        "ungoogled-chromium.mirror",
        "catacombae",
        "polyclipping",
        "usbloadergx",
        "burn-osx",
        "waircut",
        "blender-gis.mirror",
        "ancientrom",
        "jpegview",
        "butt",
        "bibdesk",
        "supertuxkart",
        "sshpass",
        "freepiano",
        "lanmsngr",
        "ext2fsd",
        "tmodloader.mirror",
        "reviews",
        "firebird",
        "emulepawcio",
        "re2c",
        "oooextras.mirror",
    }


@pytest.fixture
def mocked_sourceforge_response():

    """
    Fixture that returns a mocked response object simulating
    a successful GET request to the SourceForge projects page.
    """

    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code
            self.ok = self.status_code == 200

    def inner_mock(*args, **kwargs):
        with open(
            MOCKED_SOURCEFORGE_FILES / "sourceforge_projects_page.html",
            encoding="utf8",
        ) as f:
            return MockResponse(f.read(), 200)

    return inner_mock


class TestProjectsExtractor:
    """
    Integration and unit tests for extracting SourceForge projects and their names.
    """

    def test_extract_projects_names(self, soup, expected_projects_names) -> None:
        """
        Tests whether extract_projects_names correctly parses the project names
        from the loaded SourceForge projects HTML page.
        """
        projects = extract_projects_names(soup)
        assert projects == expected_projects_names

    def test_extract_projects_names_with_malformed_html(self):
        malformed_html = "<html><body><a href='/not-a-project/abc'>Invalid</a></body></html>"
        soup = BeautifulSoup(malformed_html, "html.parser")
        projects = extract_projects_names(soup)
        assert projects == set()

    def test_extract_projects_names_empty_page(self):
        soup = BeautifulSoup("", "html.parser")
        projects = extract_projects_names(soup)
        assert projects == set()

    def test_project_url_regex_excludes_invalid_links(self):
        regex = SourceforgeProjectsExtractor.projects_url_regex
        invalid_urls = [
            "/project/invalid",
            "/projects/",
            "/projects//extra",
            "/Projects/test",  # case-sensitive mismatch
        ]
        for url in invalid_urls:
            assert not regex.match(url)

    def test_extract(
        self,
        mocker: MockerFixture,
        mocked_sourceforge_response,
        expected_projects_names,
    ) -> None:
        """
        Tests the full extraction pipeline using a mocked HTTP request
        and a custom extractor that bypasses real project detail extraction.

        This ensures that SourceforgeProjectsExtractor correctly integrates
        with project name extraction and constructs project objects.
        """
        mock_requests_get = mocker.patch("requests.get", side_effect=mocked_sourceforge_response)

        class CustomExtractor(SourceforgeProjectExtractor):
            def extract(self, project_name: str) -> Optional[SourceforgeProject]:
                return SourceforgeProject(name=project_name, url="", code=None, subprojects=[])

        extractor = SourceforgeProjectsExtractor(CustomExtractor())
        result = extractor.extract(page_number=10)

        mock_requests_get.assert_called_once_with("https://sourceforge.net/directory/?sort=popular&page=10")
        parsed_project_names = {project.name for project in result}
        assert parsed_project_names == expected_projects_names

    def test_extract_with_failed_http(self, mocker: MockerFixture):
        mock_response = mocker.Mock(ok=False, status_code=500, text="")
        mocker.patch("requests.get", return_value=mock_response)

        extractor = SourceforgeProjectsExtractor()
        result = extractor.extract(page_number=1)
        assert result == []

    def test_extract_skips_none_projects(self, mocker: MockerFixture, mocked_sourceforge_response):
        mocker.patch("requests.get", side_effect=mocked_sourceforge_response)

        class NoneReturningExtractor(SourceforgeProjectExtractor):
            def extract(self, project_name: str) -> Optional[SourceforgeProject]:
                return None if project_name.startswith("f") else SourceforgeProject(
                    name=project_name, url="", code=None, subprojects=[]
                )

        extractor = SourceforgeProjectsExtractor(NoneReturningExtractor())
        result = extractor.extract(page_number=10)

        assert all(not p.name.startswith("f") for p in result)
