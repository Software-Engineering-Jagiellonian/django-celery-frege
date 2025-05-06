from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from frege.indexers.sourceforge.project_code_extractor import (
    GitCloneInfo,
    SourceforgeProjectCodeExtractor,
)


@dataclass
class SourceforgeSubprojects:
    """
    Represents a SourceForge subproject with a name and associated Git repository information.
    
    Attributes:
        name (str): Name of the subproject.
        code (GitCloneInfo): Git repository clone information for the subproject.
    """
    name: str
    code: GitCloneInfo


def find_subprojects_page_url(soup: BeautifulSoup) -> Optional[str]:
    """
    Finds the URL to the Git subprojects page from the given BeautifulSoup-parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the SourceForge project page.

    Returns:
        Optional[str]: URL to the subprojects Git page, or None if not found.
    """
    nav = soup.find("div", {"id": "top_nav_admin"})
    if nav is None:
        return None

    for link in nav.find_all("a"):
        if link.text.lstrip().startswith("Git"):
            href_link = link["href"][1:]  # remove '/'
            return f"https://sourceforge.net/{href_link}"
    return None


class SourceforgeSubprojectsExtractor:
    """
    Extracts Git-based subprojects from a SourceForge project page.

    Attributes:
        project_code_extractor (SourceforgeProjectCodeExtractor): 
            Optional custom extractor to retrieve Git information for subprojects.
    """

    def __init__(
        self,
        project_code_extractor: Optional[
            SourceforgeProjectCodeExtractor
        ] = None,
    ):
        """
        Initializes the extractor with an optional custom code extractor.

        Args:
            project_code_extractor (Optional[SourceforgeProjectCodeExtractor]): 
                An instance to extract Git project information. 
                If not provided, a default one is created.
        """
        self.project_code_extractor = project_code_extractor
        if self.project_code_extractor is None:
            self.project_code_extractor = SourceforgeProjectCodeExtractor()

    def extract(self, soup: BeautifulSoup) -> List[SourceforgeSubprojects]:
        """
        Extracts all Git-based subprojects from a given SourceForge project page.

        Args:
            soup (BeautifulSoup): Parsed HTML content of the main SourceForge project page.

        Returns:
            List[SourceforgeSubprojects]: A list of subproject objects with names and Git info.
        """
        result = []
        subprojects_page_url = find_subprojects_page_url(soup)
        if subprojects_page_url is None:
            return result
        response = requests.get(subprojects_page_url)
        if not response.ok:
            return result

        subprojects_page = BeautifulSoup(response.text, "html.parser")
        for link in subprojects_page.find_all("div", {"class": "list card"}):
            element = link("a")[0]
            cleaned_link = element["href"]
            if cleaned_link.startswith("/p"):
                subproject_name = element.text
                code_url = cleaned_link[1:]  # remove '/'
                code_info = self.project_code_extractor.extract(code_url)
                if code_info is None:
                    continue

                result.append(
                    SourceforgeSubprojects(
                        name=subproject_name, code=code_info
                    )
                )
        return result
