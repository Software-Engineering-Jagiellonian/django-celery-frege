"""
Utilities for interacting with Bitbucket repository data using the Bitbucket API.

This module includes functions to:
- Fetch the next created repository after a certain datetime
- Get repository metadata such as forks count, clone URL, web URL, and last commit hash
"""

import datetime
from typing import Any, NewType
from urllib import parse

import requests

__all__ = [
    "DEFAULT_DATE",
    "get_next_page",
    "get_forks_count",
    "get_clone_url",
    "get_repo_url",
    "get_last_commit_hash",
]

BITBUCKET_HOSTNAME = "bitbucket.org"
API_REPOSITORIES_ENDPOINT = "https://api.bitbucket.org/2.0/repositories"
RepositoryData = NewType("RepositoryData", dict[str, str | dict])

# Default timestamp used when no other datetime is available
DEFAULT_DATE = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def get_next_page(
    after_datetime: datetime.datetime,
) -> tuple[RepositoryData | None, datetime.datetime | None]:
    """
    Fetch the next Bitbucket repository created after a given datetime.

    Args:
        after_datetime (datetime.datetime): The timestamp after which to look for repositories.

    Returns:
        tuple: A tuple containing:
            - RepositoryData | None: The repository data dictionary or None if not found.
            - datetime.datetime | None: The datetime of the next repository, or None if not available.
    """
    after_datetime_as_iso = datetime.datetime.isoformat(after_datetime)

    response = requests.get(
        API_REPOSITORIES_ENDPOINT,
        params={"pagelen": 1, "after": after_datetime_as_iso},
    )

    if not response:
        return None, None

    response_json = response.json()

    repository_data_values = response_json.get("values")
    repository_data = (
        repository_data_values[0] if repository_data_values else None
    )

    next_url = response_json.get("next")
    new_after_datetime = (
        _parse_datetime_from_next_url(next_url) if next_url else None
    ) or datetime.datetime.utcnow()

    return repository_data, new_after_datetime


def get_forks_count(repository_data: RepositoryData) -> int:
    """
    Return the number of forks for a given repository.

    Args:
        repository_data (RepositoryData): The repository metadata dictionary.

    Returns:
        int: Number of forks, or 0 if unavailable.
    """
    url = _safe_get(repository_data, ["links", "forks", "href"])

    if not url:
        return 0

    response = requests.get(url, params={"pagelen": 0})

    if not response:
        return 0

    forks_count = response.json().get("size", 0)

    return forks_count


def get_clone_url(repository_data: RepositoryData) -> str | None:
    """
    Return the HTTPS clone URL of the repository, if hosted on Bitbucket.

    Args:
        repository_data (RepositoryData): The repository metadata dictionary.

    Returns:
        str | None: Clone URL if found and hosted on Bitbucket, otherwise None.
    """
    clone_objects = _safe_get(repository_data, ["links", "clone"]) or []

    for clone_details in clone_objects:
        clone_type = clone_details.get("name")
        clone_url = clone_details.get("href")

        # reject repositories from github.com etc.
        clone_url_host = parse.urlparse(clone_url).netloc

        if (
            clone_type in {"http", "https"}
            and clone_url_host == BITBUCKET_HOSTNAME
        ):
            return clone_url


def get_repo_url(repository_data: RepositoryData) -> str | None:
    """
    Return the URL of the repository’s webpage.

    Args:
        repository_data (RepositoryData): The repository metadata dictionary.

    Returns:
        str | None: Web URL of the repository, or None if not available.
    """
    return _safe_get(repository_data, ["links", "html", "href"])


def get_last_commit_hash(repository_data: RepositoryData) -> str | None:
    """
    Return the hash of the latest commit in the repository.

    Args:
        repository_data (RepositoryData): The repository metadata dictionary.

    Returns:
        str | None: The latest commit hash, or None if unavailable.
    """
    url = _safe_get(repository_data, ["links", "commits", "href"])

    if not url:
        return None

    response = requests.get(url, params={"pagelen": 1})

    if not response:
        return None

    commits = response.json().get("values")

    if commits:
        return commits[0].get("hash")


def _parse_datetime_from_next_url(url: str) -> datetime.datetime | None:
    """
    Extract the datetime value from the 'after' query parameter in a URL.

    Args:
        url (str): URL containing the query parameters.

    Returns:
        datetime.datetime | None: Parsed datetime object, or None if not found.
    """
    parsed_url = parse.urlparse(url)
    query_string = parse.parse_qs(parsed_url.query)
    after_params = query_string.get("after")

    if after_params:
        return datetime.datetime.fromisoformat(after_params[0])


def _safe_get(root: dict, keys: list) -> Any:
    """
    Safely access a nested value in a dictionary using a list of keys.

    Args:
        root (dict): The base dictionary.
        keys (list): List of keys to traverse.

    Returns:
        Any: The nested value if found, otherwise None.
    """
    for key in keys:
        if not root:
            break
        root = root.get(key)
    return root
