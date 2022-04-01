import abc
import os
from datetime import timedelta

import github.GithubException
from django.db import models
from django.utils.translation import gettext_lazy as _
from github import Github

from fregepoc.repositories.models import Repository
from fregepoc.utils.models import SingletonModel

indexers = []


class BaseIndexer:
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        indexers.append(cls)

    @abc.abstractmethod
    def __iter__(self):
        ...


class GitHubIndexer(SingletonModel, BaseIndexer):
    min_forks = models.PositiveIntegerField(
        _("min forks"),
        default=100,
    )
    min_stars = models.PositiveIntegerField(
        _("min stars"),
        default=100,
    )
    current_page = models.PositiveIntegerField(
        _("min stars"),
        default=0,
        help_text=_("The last visited page via GitHub API."),
    )
    rate_limit_timeout = models.DurationField(
        _("rate limit timeout"),
        default=timedelta(minutes=30),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate_limit_exceeded = False

    def __iter__(self):
        github_token = os.environ.get("GITHUB_TOKEN")
        g = Github(github_token) if github_token else Github()
        while True:
            try:
                list_of_repos = g.search_repositories(
                    query=f"forks:>={self.min_forks} stars:>={self.min_stars} is:public",
                    sort="stars",
                    page=self.current_page,
                )
                self.current_page += 1
                self.save(update_fields=["current_page"])
                repos_to_process = (
                    Repository(
                        name=repo.name,
                        description=repo.description,
                        git_url=repo.clone_url,
                        repo_url=repo.html_url,
                        commit_hash=repo.get_branch(repo.default_branch).commit.sha,
                    )
                    for repo in list_of_repos
                )
                Repository.objects.bulk_create(repos_to_process)
            except github.RateLimitExceededException:
                self.rate_limit_exceeded = True
                break
            yield from repos_to_process
