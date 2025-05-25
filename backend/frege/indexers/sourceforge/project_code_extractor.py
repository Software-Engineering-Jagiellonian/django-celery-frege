from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup


@dataclass
class GitCloneInfo:
    """
    Data class to hold Git clone information from a SourceForge project.

    Attributes:
        url (str): The Git clone URL.
        commit_hash (str): The specific commit hash or tree identifier.
    """
    url: str
    commit_hash: str


def extract_commit(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the commit hash (tree identifier) from the HTML soup.

    Args:
        soup (BeautifulSoup): Parsed HTML of the SourceForge page.

    Returns:
        Optional[str]: The commit hash if found, otherwise None.
    """
    for h2 in soup.find_all("h2"):
        if "Tree" in h2.text:
            link = h2.find("a")
            if link is None:
                return None

            return link["href"].split("/")[-2]


def extract_clone_url(soup: BeautifulSoup) -> Optional[GitCloneInfo]:
    """
    Extracts the Git clone URL and commit hash from the SourceForge project page.

    Args:
        soup (BeautifulSoup): Parsed HTML of the SourceForge project page.

    Returns:
        Optional[GitCloneInfo]: Git clone information if found, otherwise None.
    """
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
    """
    Extractor class for fetching Git clone information from a SourceForge project page.
    """
    @staticmethod
    def extract(code_url: str) -> Optional[GitCloneInfo]:
        """
        Fetches and parses a SourceForge project page to extract Git clone info.

        Args:
            code_url (str): The relative URL path to the SourceForge code page.

        Returns:
            Optional[GitCloneInfo]: Extracted Git clone information, or None if not found.
        """
        url = f"https://sourceforge.net/{code_url}"
        response = requests.get(url)
        if not response.ok:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        return extract_clone_url(soup)
