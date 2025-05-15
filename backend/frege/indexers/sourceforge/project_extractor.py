from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from frege.indexers.sourceforge.project_code_extractor import (
    GitCloneInfo,
    SourceforgeProjectCodeExtractor,
)
from frege.indexers.sourceforge.subprojects_extractor import (
    SourceforgeSubprojects,
    SourceforgeSubprojectsExtractor,
)


@dataclass
class SourceforgeProject:
    """
    Dataclass representing a SourceForge project with relevant metadata.

    Attributes:
        name (str): The name of the project.
        url (str): The URL to the project's main page on SourceForge.
        code (Optional[GitCloneInfo]): Git clone information for the main project.
        subprojects (List[SourceforgeSubprojects]): List of associated subprojects.
        description (str): A short textual description of the project.
    """
    name: str
    url: str
    code: Optional[GitCloneInfo]
    subprojects: List[SourceforgeSubprojects]
    description: str = "Unknown"


def extract_code_url(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the relative URL to the project's source code page from the HTML soup.

    Args:
        soup (BeautifulSoup): Parsed HTML of the SourceForge project page.

    Returns:
        Optional[str]: Relative path to the code page, or None if not found.
    """
    for span in soup.find_all("span"):
        if span.text == "Code":
            return span.find_parents("a")[0]["href"][1:]
    return None


def extract_description(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the project's description from the HTML soup.

    Args:
        soup (BeautifulSoup): Parsed HTML of the SourceForge project page.

    Returns:
        Optional[str]: The project description text, or None if not found.
    """
    p = soup.find("p", {"class": "description"})
    if p is None:
        return None
    return p.text


class SourceforgeProjectExtractor:
    """
    Extractor class responsible for collecting SourceForge project data,
    including subprojects, source code links, and project description.

    Attributes:
        subprojects_extractor (SourceforgeSubprojectsExtractor): Tool to extract subprojects.
        project_code_extractor (SourceforgeProjectCodeExtractor): Tool to extract project code info.
    """

    def __init__(
        self,
        subprojects_extractor: Optional[
            SourceforgeSubprojectsExtractor
        ] = None,
        project_code_extractor: Optional[
            SourceforgeProjectCodeExtractor
        ] = None,
    ):
        """
        Initializes the SourceforgeProjectExtractor with optional custom extractors.

        Args:
            subprojects_extractor (Optional[SourceforgeSubprojectsExtractor]): Custom subprojects extractor.
            project_code_extractor (Optional[SourceforgeProjectCodeExtractor]): Custom project code extractor.
        """
        self.subprojects_extractor = subprojects_extractor
        if self.subprojects_extractor is None:
            self.subprojects_extractor = SourceforgeSubprojectsExtractor(
                project_code_extractor=project_code_extractor
            )

        self.project_code_extractor = project_code_extractor
        if self.project_code_extractor is None:
            self.project_code_extractor = SourceforgeProjectCodeExtractor()

    def extract(self, project_name: str) -> Optional[SourceforgeProject]:
        """
        Extracts a complete representation of a SourceForge project.

        Args:
            project_name (str): The unique name identifier of the SourceForge project.

        Returns:
            Optional[SourceforgeProject]: Fully populated SourceforgeProject instance,
                                          or None if the project page could not be loaded.
        """
        url = f"https://sourceforge.net/projects/{project_name}"
        response = requests.get(url)
        if not response.ok:
            return None

        project_page = BeautifulSoup(response.text, "html.parser")
        main_project_code_url = extract_code_url(project_page)
        if main_project_code_url is not None:
            project_code = self.project_code_extractor.extract(main_project_code_url)
        else:
            project_code = None

        subprojects = self.subprojects_extractor.extract(project_page)
        description = extract_description(project_page)

        return SourceforgeProject(
            name=project_name,
            url=url,
            code=project_code,
            subprojects=subprojects,
            description=description if description is not None else "Unknown",
        )
