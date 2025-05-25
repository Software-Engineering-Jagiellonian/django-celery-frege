from itertools import chain
from dataclasses import dataclass

import requests
import logging

logger = logging.getLogger(__name__)

__all__ = [
    "Client",
    "RateLimitExceededException",
]

BASE_ENDPOINT = "https://gitlab.com/api/v4/projects"
PARAMS = {'pagination': 'keyset', 'per_page': '100', 'order_by': 'id', 'sort': 'asc'}


class RateLimitExceededException(Exception):
    """Exception raised when the API rate limit is exceeded."""
    pass


@dataclass
class Client:
    """
    A client for interacting with the GitLab REST API.

    Attributes:
        token (str): Optional private token for authentication.
        after_id (int): The project ID to start listing after (used for pagination).
        min_forks (int): Minimum number of forks a project must have to be included.
        min_stars (int): Minimum number of stars a project must have to be included.
        _ratelimit_remaining (int): Remaining number of requests before hitting the rate limit.
    """
    _ratelimit_remaining: int = 1000
    token: str = None
    after_id: int = 0
    min_forks: int = 0
    min_stars: int = 0

    @property
    def ratelimit_remaining(self) -> int:
        """Returns the remaining number of requests before the rate limit is exceeded."""
        return self._ratelimit_remaining

    @ratelimit_remaining.setter
    def ratelimit_remaining(self, v: str) -> None:
        """Sets the remaining rate limit count."""
        self._ratelimit_remaining = int(v)

    def repositories(self):
        """
        Generator yielding repository metadata that meets the minimum fork and star criteria.

        Yields:
            tuple: A tuple containing a dictionary of repository metadata and the project ID.
        """
        for project in chain.from_iterable(self._projects()):
            star_count = project.get('star_count', 0)
            forks_count = project.get('forks_count', 0)

            if star_count >= self.min_stars and forks_count >= self.min_forks:
                commit_hash = self._commit_hash(project['id'])
                if not commit_hash:
                    continue

                repo_data = dict(
                    name=project.get('name', 'Unnamed Project'),
                    description=project.get('description', 'No description'),
                    git_url=project.get('http_url_to_repo', ''),
                    repo_url=project.get('web_url', ''),
                    commit_hash=commit_hash
                )
                yield repo_data, project['id']

    def _get(self, *args, **kwargs):
        """
        Performs an HTTP GET request with token authentication and rate limit tracking.

        Returns:
            requests.Response: The HTTP response object.

        Raises:
            RateLimitExceededException: If the rate limit is exceeded.
        """
        if self.ratelimit_remaining <= 0:
            raise RateLimitExceededException()

        headers = {}
        if self.token:
            headers = {"PRIVATE-TOKEN": self.token}

        response = requests.get(*args, **kwargs, headers=headers)

        if 'RateLimit-Remaining' in response.headers:
            self.ratelimit_remaining = response.headers['RateLimit-Remaining']
        return response

    def _projects(self):
        """
        Generator that yields pages of projects from the GitLab API.

        Yields:
            list: A list of project JSON objects.

        Raises:
            RateLimitExceededException: If the rate limit is exceeded.
        """
        params = PARAMS
        params['id_after'] = self.after_id

        projects_response = self._get(BASE_ENDPOINT, params=params)

        if self.ratelimit_remaining <= 0:
            raise RateLimitExceededException()
        
        # returns the first page of projects
        yield projects_response.json()

        next_page = projects_response.links.get('next', {}).get('url')
        while next_page:
            projects_response = self._get(next_page)
            next_page = projects_response.links.get('next', {}).get('url')
            yield projects_response.json()

    def _commit_hash(self, project_id):
        """
        Retrieves the latest commit hash from a project's default branch.

        Args:
            project_id (int): The GitLab project ID.

        Returns:
            str or None: The commit hash, or None if unavailable.
        """
        response = self._get(f"{BASE_ENDPOINT}/{project_id}/repository/commits")

        if response.status_code != 200:
            logger.info(f"Unable to fetch commits for project {project_id}, status code: {response.status_code}")
            return None

        commits = response.json()
        if not commits:
            logger.info(f"No commits found for project {project_id}")
            return None

        mainBranch = commits[0]
        hash = mainBranch['id']

        return hash
