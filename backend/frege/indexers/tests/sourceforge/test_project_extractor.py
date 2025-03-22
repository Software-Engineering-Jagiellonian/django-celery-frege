import pytest
from bs4 import BeautifulSoup

from frege.indexers.sourceforge.project_extractor import (
    extract_code_url,
    extract_description,
)
from frege.indexers.tests.sourceforge import MOCKED_SOURCEFORGE_FILES


class TestSourceforgeProjectExtractor:
    @pytest.fixture
    def soup(self):
        with open(
            MOCKED_SOURCEFORGE_FILES / "sourceforge_project_page.html",
            encoding="utf8",
        ) as f:
            page = f.read()
        return BeautifulSoup(page, features="html.parser")

    def test_extract_code_url(self, soup) -> None:
        commit_hash = extract_code_url(soup)
        assert commit_hash == "p/schoolsplay/code/"

    def test_extract_description(self, soup) -> None:
        commit_hash = extract_description(soup)
        assert (
            commit_hash
            == "If you are looking for the childsplay application please "
            "go to http://www.childsplay.mobi"
        )
