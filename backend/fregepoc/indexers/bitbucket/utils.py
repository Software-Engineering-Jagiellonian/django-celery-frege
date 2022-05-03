import datetime as _datetime
from urllib import parse as _parse

import requests as _requests

_BITBUCKET_HOSTNAME = "bitbucket.org"
_API_REPOSITORIES_ENDPOINT = "https://api.bitbucket.org/2.0/repositories"

DEFAULT_DATE = _datetime.datetime(1970, 1, 1, tzinfo=_datetime.timezone.utc)


def get_next_page(current_date):
    current_date_as_iso = _datetime.datetime.isoformat(current_date)

    response = _requests.get(
        _API_REPOSITORIES_ENDPOINT,
        params={"pagelen": 1, "after": current_date_as_iso},
    )

    if response.status_code != 200:
        return (None, None)

    response_json = response.json()

    repository_data_values = response_json.get("values")
    next_url = response_json.get("next")

    repository_data = (
        repository_data_values[0] if repository_data_values else None
    )

    next_date = (
        _parse_date_from_next_url(next_url) or _datetime.datetime.utcnow()
    )

    return (repository_data, next_date)


def get_forks_count(repository_data):
    url = _safe_get(repository_data, ["links", "forks", "href"])

    if not url:
        return 0

    response = _requests.get(url, params={"pagelen": 0})

    if response.status_code != 200:
        return 0

    forks_count = response.json().get("size", 0)

    return forks_count


def get_clone_url(repository_data):
    clone_objects = _safe_get(repository_data, ["links", "clone"]) or []

    for clone_details in clone_objects:
        clone_type = clone_details.get("name")
        clone_url = clone_details.get("href")

        # reject repositoriest from github.com etc.
        clone_url_host = _parse.urlparse(clone_url).netloc

        if (
            clone_type in {"http", "https"}
            and clone_url_host == _BITBUCKET_HOSTNAME
        ):
            return clone_url


def get_repo_url(repository_data):
    return _safe_get(repository_data, ["links", "html", "href"])


def get_last_commit_hash(repository_data):
    url = _safe_get(repository_data, ["links", "commits", "href"])

    if not url:
        return None

    response = _requests.get(url, params={"pagelen": 1})

    if response.status_code != 200:
        return None

    commits = response.json().get("values")

    if commits:
        return commits[0].get("hash")


def _parse_date_from_next_url(url):
    parsed_url = _parse.urlparse(url)
    query_string = _parse.parse_qs(parsed_url.query)
    after_params = query_string.get("after")

    if after_params:
        return _datetime.datetime.fromisoformat(after_params[0])


def _safe_get(root, keys):
    for key in keys:
        root = root.get(key)

        if root is None:
            break

    return root
