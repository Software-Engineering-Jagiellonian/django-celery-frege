import pytest
from bs4 import BeautifulSoup

from frege.indexers.sourceforge.subprojects_extractor import find_subprojects_page_url
from frege.indexers.tests.sourceforge import MOCKED_SOURCEFORGE_FILES


@pytest.fixture(scope="module")
def soup():
    """Fixture to parse the SourceForge projects page containing subprojects."""
    with open(
        MOCKED_SOURCEFORGE_FILES / "sourceforge_projects_with_subprojects_page.html",
        encoding="utf8",
    ) as f:
        page = f.read()
    return BeautifulSoup(page, features="html.parser")


class TestSourceforgeSubprojectsExtractor:
    def test_find_subprojects_page_url(self, soup):
        """Test extraction of subprojects page URL from SourceForge."""
        expected_url = "https://sourceforge.net/p/mingw/_list/git"
        subprojects_url = find_subprojects_page_url(soup)
        
        assert subprojects_url == expected_url, (
            f"Expected URL: {expected_url}, but got: {subprojects_url}"
        )

    def test_find_subprojects_page_url_missing(self):
        """Test behavior when no subprojects page URL is found."""
        empty_soup = BeautifulSoup("", features="html.parser")
        subprojects_url = find_subprojects_page_url(empty_soup)

        assert subprojects_url is None, "Expected None when subprojects URL is missing"