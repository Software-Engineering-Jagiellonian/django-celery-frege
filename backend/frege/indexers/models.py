import os
import sys
from typing import List

import github.GithubException
import requests
from django.db import models
from django.utils.translation import gettext_lazy as _
from github import Github

from frege.indexers.base import BaseIndexer
from frege.indexers.sourceforge import SourceforgeProjectsExtractor
from frege.indexers.utils import bitbucket, gitlab
from frege.repositories.models import Repository


class GitHubIndexer(BaseIndexer):
    """
    Indexer for GitHub repositories. This class is responsible for searching and indexing
    public repositories on GitHub that meet specific criteria such as minimum forks and stars.
    
    Attributes:
        min_forks (int): Minimum number of forks required for repositories to be indexed.
        min_stars (int): Minimum number of stars required for repositories to be indexed.
        current_page (int): Tracks the current page in the GitHub API search results.
    
    Methods:
        __iter__(self): Iterates through repositories that match the specified criteria 
                         (min forks, min stars) and adds them to the database.
    """
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
        """
        Iterates through GitHub repositories matching the specified criteria (min forks,
        min stars). It fetches repositories in pages, checks if they are unique, and stores 
        them in the `Repository` model.
        
        Yields:
            List[Repository]: A list of repositories that match the criteria.
        """
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

                unique_repos = [repo for repo in list_of_repos if _is_repo_unique(repo.clone_url, self.__class__.__name__)]

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
    """
    Indexer for Sourceforge projects. This class is responsible for indexing projects 
    on Sourceforge by using the `SourceforgeProjectsExtractor` and iterating through them.
    
    Attributes:
        current_page (int): Tracks the current page in the Sourceforge project list.
        projects_extractor (SourceforgeProjectsExtractor): Extractor used to pull Sourceforge project data.
    
    Methods:
        __iter__(self): Iterates through Sourceforge projects and adds them to the database.
        main_loop(self) -> List[Repository]: Processes the project data and returns a list of repositories.
    """
    current_page = models.PositiveIntegerField(
        _("current page"),
        default=1,
        help_text=_("The last visited page."),
    )

    projects_extractor = SourceforgeProjectsExtractor()

    def __iter__(self):
        """
        Iterates through Sourceforge projects, extracting data using the `projects_extractor`.
        It adds projects to the `Repository` model and handles pagination.
        
        Yields:
            List[Repository]: A list of repositories scraped from Sourceforge.
        """
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
        """
        Extracts Sourceforge project data for the current page and processes it into
        `Repository` model instances.

        Returns:
            List[Repository]: A list of repositories processed from Sourceforge data.
        """
        projects = self.projects_extractor.extract(self.current_page)

        repos_to_process = []
        for project in projects:
            if project.code is not None:
                if not _is_repo_unique(project.code.url, self.__class__.__name__):
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
                if not _is_repo_unique(subproject.code.url, self.__class__.__name__):
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
    """
    Indexer for Bitbucket repositories. This class is responsible for indexing repositories 
    on Bitbucket based on the creation date, minimum forks, and other criteria.
    
    Attributes:
        min_forks (int): Minimum number of forks required for repositories to be indexed.
        current_date (datetime): The creation date of the repository from which to start searching.
    
    Methods:
        __iter__(self): Iterates through Bitbucket repositories and adds them to the database.
    """
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
        """
        Iterates through Bitbucket repositories, fetching them in pages and filtering based 
        on the minimum forks. Repositories are added to the `Repository` model.
        
        Yields:
            List[Repository]: A list of repositories scraped from Bitbucket.
        """
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

            if not _is_repo_unique(clone_url, self.__class__.__name__):
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
    """
    Indexer for GitLab repositories. This class is responsible for indexing GitLab repositories
    based on the minimum number of forks and stars, iterating through repositories by project ID.
    
    Attributes:
        min_forks (int): Minimum number of forks required for repositories to be indexed.
        min_stars (int): Minimum number of stars required for repositories to be indexed.
        last_project_id (int): The last processed GitLab project ID used for pagination.
    
    Methods:
        __iter__(self): Iterates through GitLab repositories and adds them to the database.
    """
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
        """
        Iterates through GitLab repositories, fetching them in pages and filtering based on 
        the minimum forks and stars. Repositories are added to the `Repository` model.
        
        Yields:
            List[Repository]: A list of repositories scraped from GitLab.
        """
        gitlab_client = gitlab.Client(
            token=os.environ.get("GITLAB_TOKEN"),
            after_id=self.last_project_id,
            min_forks=self.min_forks,
            min_stars=self.min_stars,
        )

        try:
            for repo_data, _id in gitlab_client.repositories():
                self.last_project_id = _id
                if not _is_repo_unique(repo_data["git_url"], self.__class__.__name__):
                    continue
                self.save(update_fields=["last_project_id"])
                repo_to_process = Repository.objects.create(**repo_data)

                yield [repo_to_process]
        except gitlab.RateLimitExceededException:
            self.rate_limit_exceeded = True

    class Meta:
        verbose_name = _("GitLab Indexer")
        verbose_name_plural = verbose_name


def _is_repo_unique(clone_url: str, indexer_name: str) -> bool:
    """
    Checks if a repository with the given clone URL is already in the database.

    Args:
        clone_url (str): The URL of the repository's clone.
        indexer_name (str): The name of the indexer class (used for logging purposes).

    Returns:
        bool: True if the repository is unique (not already in the database), False otherwise.
    """
    if Repository.objects.filter(git_url=clone_url).exists():
        print(f"Indexer {indexer_name} ignored crawled repository {clone_url} as it's already in the database.", file=sys.stderr)
        return False
    return True
