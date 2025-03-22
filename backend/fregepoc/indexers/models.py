import os
import sys
from typing import List

import github.GithubException
import requests
from django.db import models
from django.utils.translation import gettext_lazy as _
from github import Github

from fregepoc.indexers.base import BaseIndexer
from fregepoc.indexers.sourceforge import SourceforgeProjectsExtractor
from fregepoc.indexers.utils import bitbucket, gitlab
from fregepoc.repositories.models import Repository

class GitHubIndexer(BaseIndexer):
    min_forks = models.PositiveIntegerField(
        _("min forks"),
        default=100,
    )
    min_stars = models.PositiveIntegerField(
        _("min stars"),
        default=100,
    )
    current_page = models.PositiveIntegerField(
        _("current page"),
        default=0,
        help_text=_("The last visited page via GitHub API."),
    )

    def __iter__(self):
        github_token = os.environ.get("GITHUB_TOKEN")
        g = Github(github_token) if github_token else Github()
        while True:
            try:
                list_of_repos = g.search_repositories(
                    query=(
                        f"forks:>={self.min_forks} "
                        f"stars:>={self.min_stars} is:public"
                    ),
                    sort="stars",
                    page=self.current_page,
                )
                self.current_page += 1
                self.save(update_fields=["current_page"])

                unique_repos = [repo for repo in list_of_repos if is_repo_unique(repo.clone_url, self.__class__.__name__)]

                repos_to_process = [
                    Repository(
                        name=repo.name,
                        description=repo.description,
                        git_url=repo.clone_url,
                        repo_url=repo.html_url,
                        commit_hash=repo.get_branch(
                            repo.default_branch
                        ).commit.sha,
                    )
                    for repo in unique_repos
                ]
                Repository.objects.bulk_create(repos_to_process)
            except github.RateLimitExceededException:
                self.rate_limit_exceeded = True
                break
            yield repos_to_process

    class Meta:
        verbose_name = _("Github Indexer")
        verbose_name_plural = verbose_name


class SourceforgeIndexer(BaseIndexer):
    current_page = models.PositiveIntegerField(
        _("current page"),
        default=1,
        help_text=_("The last visited page."),
    )

    projects_extractor = SourceforgeProjectsExtractor()

    def __iter__(self):
        while True:
            try:
                yield self.main_loop()
            except requests.exceptions.RequestException:
                pass
            finally:
                self.current_page += 1
                if self.current_page >= 1000:
                    # The maximum page on the SourceForge is 999.
                    # When we reach the limit, we just start over.
                    # In the future, we may want to change by using
                    # some filters (categories) to scrap more data.
                    self.current_page = 0
                self.save(update_fields=["current_page"])

    def main_loop(self) -> List[Repository]:
        projects = self.projects_extractor.extract(self.current_page)

        repos_to_process = []
        for project in projects:
            if project.code is not None:
                if not is_repo_unique(project.code.url, self.__class__.__name__):
                    continue
                repos_to_process.append(
                    Repository(
                        name=project.name,
                        description=project.description,
                        git_url=project.code.url,
                        repo_url=project.url,
                        commit_hash=project.code.commit_hash,
                    )
                )

            for subproject in project.subprojects:
                if not is_repo_unique(subproject.code.url, self.__class__.__name__):
                    continue
                repos_to_process.append(
                    Repository(
                        name=f"{project.name}/{subproject.name}",
                        description=project.description,
                        git_url=subproject.code.url,
                        repo_url=project.url,
                        commit_hash=subproject.code.commit_hash,
                    )
                )

        Repository.objects.bulk_create(repos_to_process)
        return repos_to_process

    class Meta:
        verbose_name = _("Sourceforge Indexer")
        verbose_name_plural = verbose_name


class BitbucketIndexer(BaseIndexer):
    min_forks = models.PositiveIntegerField(
        _("min forks"),
        default=1,
    )

    current_date = models.DateTimeField(
        _("current date"),
        default=bitbucket.DEFAULT_DATE,
        help_text=_(
            "The creation date of repository from which to start searching. "
            "Please note that Bitbucket API paginates repos by creation date, "
            "so the dates are used to iterate over repositories."
        ),
    )

    def __iter__(self):
        while True:
            repository_data, next_date = bitbucket.get_next_page(
                self.current_date
            )

            if not repository_data:
                self.rate_limit_exceeded = True
                break

            self.current_date = next_date
            self.save(update_fields=["current_date"])

            if (
                self.min_forks
                and bitbucket.get_forks_count(repository_data) < self.min_forks
            ):
                continue

            clone_url = bitbucket.get_clone_url(repository_data)
            repo_url = bitbucket.get_repo_url(repository_data)
            commit_hash = bitbucket.get_last_commit_hash(repository_data)

            if not (clone_url and repo_url and commit_hash):
                continue

            if not is_repo_unique(clone_url, self.__class__.__name__):
                continue

            repo_to_process = Repository.objects.create(
                name=repository_data.get("name"),
                description=repository_data.get("description"),
                git_url=clone_url,
                repo_url=repo_url,
                commit_hash=commit_hash,
            )

            yield [repo_to_process]

    class Meta:
        verbose_name = _("Bitbucket Indexer")
        verbose_name_plural = verbose_name


class GitLabIndexer(BaseIndexer):
    min_forks = models.PositiveIntegerField(
        _("min forks"),
        default=1,
    )
    min_stars = models.PositiveIntegerField(
        _("min stars"),
        default=0,
    )

    last_project_id = models.PositiveIntegerField(
        _("last project id"),
        default=0,
        help_text=_("The last processed project id."),
    )

    def __iter__(self):
        gitlab_client = gitlab.Client(
            token=os.environ.get("GITLAB_TOKEN"),
            after_id=self.last_project_id,
            min_forks=self.min_forks,
            min_stars=self.min_stars,
        )

        try:
            for repo_data, _id in gitlab_client.repositories():
                self.last_project_id = _id
                if not is_repo_unique(repo_data["git_url"], self.__class__.__name__):
                    continue
                self.save(update_fields=["last_project_id"])
                repo_to_process = Repository.objects.create(**repo_data)

                yield [repo_to_process]
        except gitlab.RateLimitExceededException:
            self.rate_limit_exceeded = True

    class Meta:
        verbose_name = _("GitLab Indexer")
        verbose_name_plural = verbose_name

def is_repo_unique(clone_url: str, indexer_name: str) -> bool:
    if Repository.objects.filter(git_url=clone_url).exists():
        print(f"Indexer {indexer_name} ignored crawled repository {clone_url} as it's already in the database.", file=sys.stderr)
        return False
    return True
