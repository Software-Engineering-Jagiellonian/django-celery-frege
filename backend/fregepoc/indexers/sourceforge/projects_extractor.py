import re
from typing import Optional, List

import requests
from bs4 import BeautifulSoup

from fregepoc.indexers.sourceforge.project_extractor import SourceforgeProjectExtractor, SourceforgeProject


def extract_projects_names(soup: BeautifulSoup) -> set[str]:
    projects_set = set()
    for link in soup.find_all('a', href=SourceforgeProjectsExtractor.projects_url_regex):
        projects_set.add(link['href'].split('/')[-2])

    return projects_set


class SourceforgeProjectsExtractor:
    projects_url_regex = re.compile(r'/projects/\w+')

    def __init__(self, project_extractor: Optional[SourceforgeProjectExtractor] = None):
        self.project_extractor = project_extractor
        if self.project_extractor is None:
            self.project_extractor = SourceforgeProjectExtractor()

    def extract(self, page_number: int) -> List[SourceforgeProject]:
        result = []
        url = f'https://sourceforge.net/directory/?sort=popular&page={page_number}'
        response = requests.get(url)
        if not response.ok:
            return result

        soup = BeautifulSoup(response.text, 'html.parser')
        for project_name in extract_projects_names(soup):
            extracted_project = self.project_extractor.extract(project_name)
            if extracted_project is not None:
                result.append(extracted_project)

        return result
