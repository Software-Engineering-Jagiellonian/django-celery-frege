import pytest
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock

from frege.indexers.sourceforge.project_extractor import (
    extract_code_url,
    extract_description,
    SourceforgeProjectExtractor,
)
from frege.indexers.tests.sourceforge import MOCKED_SOURCEFORGE_FILES


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

    def test_project_extractor_http_fail(self):
        mock_response = MagicMock()
        mock_response.ok = False

        with patch("requests.get", return_value=mock_response):
            extractor = SourceforgeProjectExtractor()
            project = extractor.extract("nonexistent-project")

        assert project is None

    def test_project_extractor_no_code_or_description(self):
        html = "<html><body><div>No code or description here</div></body></html>"

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = html

        with patch("requests.get", return_value=mock_response):
            extractor = SourceforgeProjectExtractor()
            project = extractor.extract("someproject")

        assert project is not None
        assert project.code is None
        assert project.description == "Unknown"
        assert isinstance(project.subprojects, list)

    def test_custom_extractor_initialization(self):
        mock_subprojects_extractor = MagicMock()
        mock_code_extractor = MagicMock()

        extractor = SourceforgeProjectExtractor(
            subprojects_extractor=mock_subprojects_extractor,
            project_code_extractor=mock_code_extractor,
        )

        assert extractor.subprojects_extractor == mock_subprojects_extractor
        assert extractor.project_code_extractor == mock_code_extractor
