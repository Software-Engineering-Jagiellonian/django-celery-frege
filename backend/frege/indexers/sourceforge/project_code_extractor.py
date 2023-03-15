from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup


@dataclass
class GitCloneInfo:
    url: str
    commit_hash: str


def extract_commit(soup: BeautifulSoup) -> Optional[str]:
    for h2 in soup.find_all("h2"):
        if "Tree" in h2.text:
            link = h2.find("a")
            if link is None:
                return None

            return link["href"].split("/")[-2]


def extract_clone_url(soup: BeautifulSoup) -> Optional[GitCloneInfo]:
    value = soup.find("input", {"id": "access_url"})
    if value:
        value = value.get("value")
        if value.startswith("git clone"):
            git_link = value.split()[2]
            commit_hash = extract_commit(soup)

            if commit_hash is None:
                return None

            return GitCloneInfo(url=git_link, commit_hash=commit_hash)
    return None


class SourceforgeProjectCodeExtractor:
    @staticmethod
    def extract(code_url: str) -> Optional[GitCloneInfo]:
        url = f"https://sourceforge.net/{code_url}"
        response = requests.get(url)
        if not response.ok:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        return extract_clone_url(soup)
