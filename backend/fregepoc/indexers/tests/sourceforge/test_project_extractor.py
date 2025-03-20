import pytest
from bs4 import BeautifulSoup

from fregepoc.indexers.sourceforge.project_extractor import (
    extract_code_url,
    extract_description,
)
from fregepoc.indexers.tests.sourceforge import MOCKED_SOURCEFORGE_FILES


class TestSourceforgeProjectExtractor:
    @pytest.fixture(scope="module")
    def soup(self):
        with open(
            MOCKED_SOURCEFORGE_FILES / "sourceforge_project_page.html",
            encoding="utf8",
        ) as f:
            page = f.read()
        return BeautifulSoup(page, features="html.parser")

    def test_extract_code_url(self, soup) -> None:
        code_url = extract_code_url(soup)
        expected_url = "p/schoolsplay/code/"
        assert code_url == expected_url, f"Expected {expected_url}, got {code_url}"

    def test_extract_description(self, soup) -> None:
        description = extract_description(soup)
        expected_description = (
            "If you are looking for the childsplay application please "
            "go to http://www.childsplay.mobi"
        )
        assert description == expected_description, (
            f"Expected description:\n{expected_description}\n"
            f"But got:\n{description}"
        )

    def test_extract_code_url_missing(self, soup) -> None:
        for tag in soup.find_all():
            tag.extract()

        code_url = extract_code_url(soup)
        assert code_url is None, "Expected None when the code URL is missing"

    def test_extract_description_missing(self, soup) -> None:
        for tag in soup.find_all():
            tag.extract()

        description = extract_description(soup)
        assert description is None, "Expected None when the description is missing"
