from typing import Optional

import pytest
import requests
from bs4 import BeautifulSoup
from pytest_mock import MockerFixture

from fregepoc.indexers.sourceforge.project_extractor import (
    SourceforgeProject,
    SourceforgeProjectExtractor,
)
from fregepoc.indexers.sourceforge.projects_extractor import (
    SourceforgeProjectsExtractor,
    extract_projects_names,
)
from fregepoc.indexers.tests.sourceforge.constants import MOCKED_SOURCEFORGE_FILES


@pytest.fixture(scope="module")
def soup():
    with open(
        MOCKED_SOURCEFORGE_FILES / "sourceforge_projects_page.html",
        encoding="utf8",
    ) as f:
        page = f.read()
    return BeautifulSoup(page, features="html.parser")


@pytest.fixture(scope="module")
def expected_projects_names():
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
    def test_extract_projects_names(self, soup, expected_projects_names) -> None:
        projects = extract_projects_names(soup)
        assert projects == expected_projects_names, (
            f"Extracted projects do not match expected names.\n"
            f"Expected: {expected_projects_names}\n"
            f"Got: {projects}"
        )

    def test_extract(self, mocker: MockerFixture, mocked_sourceforge_response, expected_projects_names) -> None:
        mock_requests_get = mocker.patch("requests.get", side_effect=mocked_sourceforge_response)

        class CustomSourceforgeProjectExtractor(SourceforgeProjectExtractor):
            """Custom extractor returning projects without actual scraping."""

            def extract(self, project_name: str) -> Optional[SourceforgeProject]:
                return SourceforgeProject(name=project_name, url="", code=None, subprojects=[])

        extractor = SourceforgeProjectsExtractor(CustomSourceforgeProjectExtractor())

        result = extractor.extract(page_number=10)
        mock_requests_get.assert_called_once_with(f"https://sourceforge.net/directory/?sort=popular&page=10")

        parsed_project_names = {project.name for project in result}

        assert parsed_project_names == expected_projects_names, (
            f"Extracted project names do not match expected values.\n"
            f"Expected: {expected_projects_names}\n"
            f"Got: {parsed_project_names}"
        )
