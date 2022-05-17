from dataclasses import dataclass
from typing import Optional, List

import requests
from bs4 import BeautifulSoup

from fregepoc.indexers.sourceforge.project_code_extractor import SourceforgeProjectCodeExtractor, GitCloneInfo


@dataclass
class SourceforgeSubprojects:
    name: str
    code: GitCloneInfo


def find_subprojects_page_url(soup: BeautifulSoup) -> Optional[str]:
    nav = soup.find('div', {'id': 'top_nav_admin'})
    if nav is None:
        return None

    for link in nav.find_all('a'):
        if link.text.lstrip().startswith('Git'):
            href_link = link['href'][1:]  # remove '/'
            return f'https://sourceforge.net/{href_link}'
    return None


class SourceforgeSubprojectsExtractor:
    def __init__(self, project_code_extractor: Optional[SourceforgeProjectCodeExtractor] = None):
        self.project_code_extractor = project_code_extractor
        if self.project_code_extractor is None:
            self.project_code_extractor = SourceforgeProjectCodeExtractor()

    def extract(self, soup: BeautifulSoup) -> List[SourceforgeSubprojects]:
        result = []
        subprojects_page_url = find_subprojects_page_url(soup)
        if subprojects_page_url is None:
            return result
        response = requests.get(subprojects_page_url)
        if not response.ok:
            return result

        subprojects_page = BeautifulSoup(response.text, 'html.parser')
        for link in subprojects_page.find_all('div', {'class': 'list card'}):
            element = link('a')[0]
            cleaned_link = element['href']
            if cleaned_link.startswith('/p'):
                subproject_name = element.text
                code_url = cleaned_link[1:]  # remove '/'
                code_info = self.project_code_extractor.extract(code_url)
                if code_info is None:
                    continue

                result.append(
                    SourceforgeSubprojects(
                        name=subproject_name,
                        code=code_info
                    )
                )
        return result
