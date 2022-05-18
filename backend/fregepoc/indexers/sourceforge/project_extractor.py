from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from fregepoc.indexers.sourceforge.project_code_extractor import (
    GitCloneInfo,
    SourceforgeProjectCodeExtractor,
)
from fregepoc.indexers.sourceforge.subprojects_extractor import (
    SourceforgeSubprojects,
    SourceforgeSubprojectsExtractor,
)


@dataclass
class SourceforgeProject:
    name: str
    url: str
    code: Optional[GitCloneInfo]
    subprojects: List[SourceforgeSubprojects]
    description: str = "Unknown"


def _extract_code_url(soup: BeautifulSoup) -> Optional[str]:
    for span in soup.find_all("span"):
        if span.text == "Code":
            return span.find_parents("a")[0]["href"][1:]
    return None


def _extract_description(soup: BeautifulSoup) -> Optional[str]:
    p = soup.find("p", {"class": "description"})
    if p is None:
        return None
    return p.text


class SourceforgeProjectExtractor:
    def __init__(
        self,
        subprojects_extractor: Optional[
            SourceforgeSubprojectsExtractor
        ] = None,
        project_code_extractor: Optional[
            SourceforgeProjectCodeExtractor
        ] = None,
    ):
        self.subprojects_extractor = subprojects_extractor
        if self.subprojects_extractor is None:
            self.subprojects_extractor = SourceforgeSubprojectsExtractor(
                project_code_extractor=project_code_extractor
            )

        self.project_code_extractor = project_code_extractor
        if self.project_code_extractor is None:
            self.project_code_extractor = SourceforgeProjectCodeExtractor()

    def extract(self, project_name: str) -> Optional[SourceforgeProject]:
        url = f"https://sourceforge.net/projects/{project_name}"
        response = requests.get(url)
        if not response.ok:
            return None

        project_page = BeautifulSoup(response.text, "html.parser")
        main_project_code_url = _extract_code_url(project_page)
        if main_project_code_url is not None:
            project_code = self.project_code_extractor.extract(
                main_project_code_url
            )
        else:
            project_code = None

        subprojects = self.subprojects_extractor.extract(project_page)
        description = _extract_description(project_page)

        return SourceforgeProject(
            name=project_name,
            url=url,
            code=project_code,
            subprojects=subprojects,
            description=description if description is not None else "Unknown",
        )
