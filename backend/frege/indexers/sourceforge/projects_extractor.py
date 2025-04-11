import re
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from frege.indexers.sourceforge.project_extractor import (
    SourceforgeProject,
    SourceforgeProjectExtractor,
)


def extract_projects_names(soup: BeautifulSoup) -> set[str]:
    """
    Extracts the names of SourceForge projects from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A parsed HTML document.

    Returns:
        set[str]: A set of project names extracted from the page.
    """
    projects_set = set()
    for link in soup.find_all(
        "a", href=SourceforgeProjectsExtractor.projects_url_regex
    ):
        projects_set.add(link["href"].split("/")[-2])

    return projects_set


class SourceforgeProjectsExtractor:
    """
    Extracts a list of SourceForge projects from the SourceForge directory pages.

    Attributes:
        projects_url_regex (Pattern): A regex pattern to match SourceForge project URLs.
        project_extractor (SourceforgeProjectExtractor): An instance used to extract individual project details.
    """
    projects_url_regex = re.compile(r"/projects/\w+")

    def __init__(
        self, project_extractor: Optional[SourceforgeProjectExtractor] = None
    ):
        """
        Initializes the SourceforgeProjectsExtractor.

        Args:
            project_extractor (Optional[SourceforgeProjectExtractor]): Optional custom project extractor.
                If not provided, a default instance of SourceforgeProjectExtractor is used.
        """
        self.project_extractor = project_extractor
        if self.project_extractor is None:
            self.project_extractor = SourceforgeProjectExtractor()

    def extract(self, page_number: int) -> List[SourceforgeProject]:
        """
        Extracts SourceForge projects from a specific directory page.

        Args:
            page_number (int): The directory page number to extract projects from.

        Returns:
            List[SourceforgeProject]: A list of extracted project objects.
        """
        result = []
        query = f"sort=popular&page={page_number}"
        url = f"https://sourceforge.net/directory/?{query}"
        response = requests.get(url)
        if not response.ok:
            return result

        soup = BeautifulSoup(response.text, "html.parser")
        for project_name in extract_projects_names(soup):
            extracted_project = self.project_extractor.extract(project_name)
            if extracted_project is not None:
                result.append(extracted_project)

        return result
