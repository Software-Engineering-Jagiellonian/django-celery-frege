import itertools
import os

import github.GithubException
from django.db import models
from django.utils.translation import gettext_lazy as _
from github import Github

from fregepoc.indexers.base import BaseIndexer
from fregepoc.repositories.models import Repository

from fregepoc.indexers.sourceforge import SinglePageProjectsExtractor
from fregepoc.indexers.sourceforge import SingleProjectCodeUrlExtractor
from fregepoc.indexers.sourceforge import SingleProjectGitLinkExtractor
from fregepoc.indexers.sourceforge import SingleProjectGitUrlExtractor
from fregepoc.indexers.sourceforge import SingleProjectResponseExtractor


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
                    for repo in list_of_repos
                ]
                Repository.objects.bulk_create(repos_to_process)
            except github.RateLimitExceededException:
                self.rate_limit_exceeded = True
                break
            yield from repos_to_process

    class Meta:
        verbose_name = _("Github Indexer")
        verbose_name_plural = verbose_name


class SourceforgeIndexer(BaseIndexer):
    current_page = models.PositiveIntegerField(
        _("current page"),
        default=1,
        help_text=_("The last visited page."),
    )

    singlePageProjectsExtractor = SinglePageProjectsExtractor()
    singleProjectCodeUrlExtractor = SingleProjectCodeUrlExtractor()
    singleProjectGitLinkExtractor = SingleProjectGitLinkExtractor()
    singleProjectResponseExtractor = SingleProjectResponseExtractor()
    singleProjectGitUrlExtractor = SingleProjectGitUrlExtractor()

    def __iter__(self):
        for i in itertools.count(start=self.current_page):
            projects = self.singlePageProjectsExtractor.extract(i)

            self.current_page += 1
            self.save(update_fields=["current_page"])

            if not projects:
                continue

            for project_name in projects:
                repos_to_process = []

                single_project_soup = self.singleProjectResponseExtractor.extract(project_name)

                project_code_url = self.singleProjectCodeUrlExtractor.extract(single_project_soup)
                repo_from_code_url = self.handle_code_url(project_name, project_code_url)
                if repo_from_code_url is not None:
                    repos_to_process.append(repo_from_code_url)

                project_git_ulr = self.singleProjectGitUrlExtractor.extract(single_project_soup)
                repos_to_process.extend(self.handle_git_url(project_name, project_git_ulr))

                Repository.objects.bulk_create(repos_to_process)
                yield from repos_to_process

    def handle_code_url(self, project_name, project_code_url):
        if project_code_url is None:
            return None

        project_git_url_from_code_url = self.singleProjectGitLinkExtractor.extract(project_code_url)
        if project_git_url_from_code_url is None:
            return None

        return Repository(
            name=project_name,
            description=project_name,
            git_url=project_git_url_from_code_url,
            repo_url=project_code_url,
            commit_hash="HEAD",  # TODO
        )

    def handle_git_url(self, project_name, project_git_urls):
        extracted_git_url = [
            (
                subproject,
                self.singleProjectGitLinkExtractor.extract(git_url)
            )
            for (subproject, git_url) in project_git_urls
        ]

        return [
            Repository(
                name=f"{project_name}/{subproject}",
                description=project_name,
                git_url=git_url,
                repo_url=git_url,  # TODO
                commit_hash="HEAD",  # TODO
            )
            for (subproject, git_url) in extracted_git_url if git_url is not None
        ]

    class Meta:
        verbose_name = _("Sourceforge Indexer")
        verbose_name_plural = verbose_name
