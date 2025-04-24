import os
import pytest
from unittest import mock
from frege.indexers.models import GitHubIndexer
from frege.repositories.models import Repository
from github import Github
from github import RateLimitExceededException
from github.Repository import Repository as GHRepo
from github.Branch import Branch
from django.db import IntegrityError

@pytest.fixture
def github_indexer():
    return GitHubIndexer.objects.create(min_forks=200, min_stars=300, current_page=0)

def mock_repo(name="test-repo", sha="abc123"):
    mock_branch = mock.create_autospec(Branch)
    mock_branch.commit.sha = sha

    mock_repo = mock.create_autospec(GHRepo)
    mock_repo.name = name
    mock_repo.description = "Test repo"
    mock_repo.clone_url = f"https://github.com/test/{name}.git"
    mock_repo.html_url = f"https://github.com/test/{name}"
    mock_repo.default_branch = "main"
    mock_repo.get_branch.return_value = mock_branch
    return mock_repo

@mock.patch("frege.indexers.models._is_repo_unique", return_value=True)
@mock.patch("frege.indexers.models.Repository.objects.bulk_create")
@mock.patch("frege.indexers.models.Github")
@pytest.mark.django_db
def test_iter_creates_repositories(mock_github_cls, mock_bulk_create, mock_unique, github_indexer):
    mock_github = mock.Mock()
    mock_repo_obj = mock_repo()
    mock_github.search_repositories.return_value = [mock_repo_obj]
    mock_github_cls.return_value = mock_github

    iterator = iter(github_indexer)
    created_repos = next(iterator)

    mock_github.search_repositories.assert_called_once_with(
        query="forks:>=200 stars:>=300 is:public",
        sort="stars",
        page=0
    )
    assert github_indexer.current_page == 1
    mock_bulk_create.assert_called_once()
    assert len(created_repos) == 1

@mock.patch.dict(os.environ, {}, clear=True)
@mock.patch("frege.indexers.models.Github")
@pytest.mark.django_db
def test_iter_uses_no_token(mock_github_cls, github_indexer):
    iter(github_indexer)
    mock_github_cls.assert_not_called()


@mock.patch("frege.indexers.models._is_repo_unique", return_value=True)
@mock.patch("frege.indexers.models.Repository.objects.bulk_create")
@mock.patch("frege.indexers.models.Github")
@pytest.mark.django_db
def test_repository_field_mapping(mock_github_cls, mock_bulk_create, mock_unique, github_indexer):
    mock_github = mock.Mock()
    mock_repo_obj = mock_repo(name="test-repo", sha="test-sha")
    mock_github.search_repositories.return_value = [mock_repo_obj]
    mock_github_cls.return_value = mock_github

    iterator = iter(github_indexer)
    next(iterator)
    
    created_repos = mock_bulk_create.call_args[0][0]
    assert len(created_repos) == 1
    repo = created_repos[0]
    assert repo.name == "test-repo"
    assert repo.git_url == "https://github.com/test/test-repo.git"
    assert repo.repo_url == "https://github.com/test/test-repo"
    assert repo.commit_hash == "test-sha"

@mock.patch("frege.indexers.models._is_repo_unique", return_value=True)
@mock.patch("frege.indexers.models.Repository.objects.bulk_create")
@mock.patch("frege.indexers.models.Github")
@pytest.mark.django_db
def test_query_construction(mock_github_cls, mock_bulk_create, mock_unique, github_indexer):
    mock_github = mock.Mock()
    mock_github.search_repositories.return_value = []
    mock_github_cls.return_value = mock_github

    github_indexer.min_forks = 150
    github_indexer.min_stars = 250
    iterator = iter(github_indexer)
    next(iterator)
    
    mock_github.search_repositories.assert_called_once_with(
        query="forks:>=150 stars:>=250 is:public",
        sort="stars",
        page=0
    )

@mock.patch("frege.indexers.models.Github")
@pytest.mark.django_db
def test_iter_handles_rate_limit(mock_github_cls, github_indexer):
    mock_github = mock.Mock()
    mock_github.search_repositories.side_effect = RateLimitExceededException(403, "Rate limited", headers={})
    mock_github_cls.return_value = mock_github

    iterator = iter(github_indexer)
    with pytest.raises(StopIteration):
        next(iterator)
    
    assert github_indexer.rate_limit_exceeded is True