import re

import requests
from bs4 import BeautifulSoup


class SinglePageProjectsExtractor:
    @staticmethod
    def extract(page_number):
        if page_number <= 0:
            return None
        url = f"https://sourceforge.net/directory/?sort=popular&page={page_number}"
        response = requests.get(url)

        if response.status_code == 404:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        projects_set = set()
        for link in soup.find_all("a", href=re.compile(r"/projects/\w+")):
            projects_set.add("/".join(link["href"].split("/")[:3])[1:])

        return projects_set
