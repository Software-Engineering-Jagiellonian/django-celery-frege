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
from fregepoc.indexers.tests.sourceforge.constants import (
    MOCKED_SOURCEFORGE_FILES,
)


def mocked_sourceforge_response():
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code
            self.ok = True if self.status_code == 200 else False

    def inner_mock(*args, **kwargs):
        with open(
            MOCKED_SOURCEFORGE_FILES / "sourceforge_projects_page.html",
            encoding="utf8",
        ) as f:
            return MockResponse(f.read(), 200)

    return inner_mock


class TestProjectsExtractor:
    @pytest.fixture
    def expected_projects_names(self):
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

    def test_extract_projects_names(self, expected_projects_names) -> None:
        with open(
            MOCKED_SOURCEFORGE_FILES / "sourceforge_projects_page.html",
            encoding="utf8",
        ) as f:
            page = f.read()

        soup = BeautifulSoup(page, features="html.parser")
        projects = extract_projects_names(soup)

        assert projects == expected_projects_names

    def test_extract(
        self, mocker: MockerFixture, expected_projects_names
    ) -> None:
        mocker.patch(
            "requests.get",
            side_effect=mocked_sourceforge_response(),
        )

        class CustomSourceforgeProjectExtractor(SourceforgeProjectExtractor):
            def extract(
                self, project_name: str
            ) -> Optional[SourceforgeProject]:
                return SourceforgeProject(
                    name=project_name, url="", code=None, subprojects=[]
                )

        extractor = SourceforgeProjectsExtractor(
            CustomSourceforgeProjectExtractor()
        )

        result = extractor.extract(page_number=10)
        requests.get.assert_called_once_with(
            f"https://sourceforge.net/directory/?sort=popular&page={10}"
        )
        parsed_result = set(map(lambda x: x.name, result))

        assert parsed_result == expected_projects_names
