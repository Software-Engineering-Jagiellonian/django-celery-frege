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

DEFAULT_DATE = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def get_next_page(
    after_datetime: datetime.datetime,
) -> tuple[RepositoryData | None, datetime.datetime | None]:
    """
    Fetches the next repository created after a given datetime.

    Returns data concerning the repository and a datetime that can be used to
    fetch the next one.
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
    """Retuns the number of forks of given repository or `0` on error."""
    url = _safe_get(repository_data, ["links", "forks", "href"])

    if not url:
        return 0

    response = requests.get(url, params={"pagelen": 0})

    if not response:
        return 0

    forks_count = response.json().get("size", 0)

    return forks_count


def get_clone_url(repository_data: RepositoryData) -> str | None:
    """Retuns the clone URL for a repository if it's hosted on BitBucket."""
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
    """Retuns the URL of a repository's webpage."""
    return _safe_get(repository_data, ["links", "html", "href"])


def get_last_commit_hash(repository_data: RepositoryData) -> str | None:
    """Retuns the SHA256 hash of the repository's latest commit."""
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
    Given a URL, parses the datetime included as its querystring parameter.

    The datetime is expected to be present under 'after' parameter and
    represented in ISO 8601 format.
    """
    parsed_url = parse.urlparse(url)
    query_string = parse.parse_qs(parsed_url.query)
    after_params = query_string.get("after")

    if after_params:
        return datetime.datetime.fromisoformat(after_params[0])


def _safe_get(root: dict, keys: list) -> Any:
    """
    Given a (nested) dictionary and a list of keys, returns a nested value.

    The function will traverse the dictionary on key-by-key manner, returning
    the last value. Returns None immediately if encounters a falsy value.
    """
    for key in keys:
        if not root:
            break

        root = root.get(key)

    return root
