import requests
from bs4 import BeautifulSoup


class SingleProjectResponseExtractor:
    @staticmethod
    def extract(project_name):
        if not project_name:
            return

        url = f"https://sourceforge.net/{project_name}"
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")
