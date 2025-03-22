from bs4 import BeautifulSoup

from frege.indexers.sourceforge.subprojects_extractor import (
    find_subprojects_page_url,
)
from frege.indexers.tests.sourceforge import MOCKED_SOURCEFORGE_FILES


class TestSourceforgeSubprojectsExtractor:
    def test_find_subprojects_page_url(self):
        with open(
            MOCKED_SOURCEFORGE_FILES
            / "sourceforge_projects_with_subprojects_page.html",
            encoding="utf8",
        ) as f:
            page = f.read()
        soup = BeautifulSoup(page, features="html.parser")
        subprojects_url = find_subprojects_page_url(soup)
        assert subprojects_url == "https://sourceforge.net/p/mingw/_list/git"
