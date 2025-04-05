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
    pass


@dataclass
class Client:
    """Class for communication with the GitLab REST API"""
    _ratelimit_remaining: int = 1000
    token: str = None
    after_id: int = 0
    min_forks: int = 0
    min_stars: int = 0

    @property
    def ratelimit_remaining(self) -> int:
        return self._ratelimit_remaining

    @ratelimit_remaining.setter
    def ratelimit_remaining(self, v: str) -> None:
        self._ratelimit_remaining = int(v)

    def repositories(self):     
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
        """HTTP GET method with checking ratelimit and adding token"""
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
        """Lists JSON array with projects"""
        params = PARAMS
        params['id_after'] = self.after_id

        projects_response = self._get(BASE_ENDPOINT, params=params)

        if self.ratelimit_remaining <= 0:
            raise RateLimitExceededException()

        next_page = projects_response.links.get('next', {}).get('url')
        while next_page:
            projects_response = self._get(next_page)
            next_page = projects_response.links.get('next', {}).get('url')
            yield projects_response.json()

    def _commit_hash(self, project_id):
        url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/commits"
        response = self._get(url)

        if response.status_code != 200:
            logger.warning(f"Unable to fetch commits for project {project_id}, status code: {response.status_code}")
            return None

        commits = response.json()
        if not commits:
            logger.warning(f"No commits found for project {project_id}")
            return None

        return commits[0]['id']
