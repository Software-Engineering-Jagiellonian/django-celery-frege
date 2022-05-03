import datetime as _datetime
import urllib.parse as _parse

import requests as _requests

_API_URL = "https://api.bitbucket.org/2.0/repositories"
DEFAULT_DATE = _datetime.datetime(1970, 1, 1, tzinfo=_datetime.timezone.utc)


def get_next_repo(current_date):
    response = _requests.get(
        _API_URL, params={"pagelen": 1, "after": str(current_date)}
    )

    return _get_response_first_value(response)


def parse_next_date(url):
    return _parse.parse_qs(_parse.urlparse(url)).get("after")


def get_forks_count(repository_data):
    url = _safe_get(repository_data, ["links", "forks", "href"])

    if not url:
        return 0

    response = _requests.get(url, params={"pagelen": 0})

    if response.status_code != 200:
        return 0

    return response.json().get("size", 0)


def get_clone_url(repository_data):
    clone_objects = _safe_get(repository_data, ["links", "clone"])

    for clone_details in clone_objects:
        if clone_details["name"] in ["http", "https"]:
            return clone_details["href"]
    else:
        return None


def get_repo_url(repository_data):
    return _safe_get(repository_data, ["links", "html", "href"]) or ""


def get_last_commit_hash(repository_data):
    url = _safe_get(repository_data, ["links", "commits", "href"])

    if not url:
        return None

    response = _requests.get(url, params={"pagelen": 1})
    last_commit = _get_response_first_value(response)

    if last_commit:
        return last_commit["hash"]
    else:
        return None


def _get_response_first_value(response):
    if response.status_code != 200:
        return None

    values = response.json()["values"]

    if not values:
        return None

    return values[0]


def _safe_get(root, keys):
    for key in keys:
        root = root.get(key, {})

    return root
