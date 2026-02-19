"""
Unit tests for indexer error handling in frege.indexers.models.

Covers:
- GitLabIndexer: cursor save order, create() failure handling
- BitbucketIndexer: cursor save order, create() failure handling
- GitHubIndexer: cursor save order, bulk_create() failure handling, rate limit
"""

import pytest
from unittest.mock import patch, MagicMock, Mock, PropertyMock, call
from django.db import IntegrityError


MODULE = "frege.indexers.models"


@pytest.mark.django_db
class TestGitLabIndexerErrorHandling:
    """Tests for GitLabIndexer.__iter__() error handling."""

    @patch(f"{MODULE}.gitlab.Client")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.create")
    def test_saves_cursor_after_create(self, mock_create, mock_unique, mock_client_cls):
        """save(last_project_id) should happen AFTER successful create()."""
        from frege.indexers.models import GitLabIndexer

        mock_repo = Mock()
        mock_create.return_value = mock_repo

        mock_client = Mock()
        mock_client.repositories.return_value = iter([
            ({"git_url": "http://example.com/repo1.git", "name": "repo1"}, 100),
        ])
        mock_client_cls.return_value = mock_client

        call_order = []

        def track_create(**kwargs):
            call_order.append("create")
            return mock_repo
        mock_create.side_effect = track_create

        indexer = GitLabIndexer()

        with patch.object(GitLabIndexer, "save", side_effect=lambda **kw: call_order.append("save")):
            list(indexer)

        assert "create" in call_order
        assert "save" in call_order
        assert call_order.index("create") < call_order.index("save")

    @patch(f"{MODULE}.gitlab.Client")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.create")
    def test_create_failure_saves_cursor_and_continues(
        self, mock_create, mock_unique, mock_client_cls
    ):
        """IntegrityError on create() should save cursor and continue to next repo."""
        from frege.indexers.models import GitLabIndexer

        mock_repo = Mock()
        mock_create.side_effect = [IntegrityError("duplicate"), mock_repo]

        mock_client = Mock()
        mock_client.repositories.return_value = iter([
            ({"git_url": "http://example.com/repo1.git", "name": "repo1"}, 100),
            ({"git_url": "http://example.com/repo2.git", "name": "repo2"}, 200),
        ])
        mock_client_cls.return_value = mock_client

        indexer = GitLabIndexer()
        with patch.object(GitLabIndexer, "save"):
            results = list(indexer)

        # Second repo should succeed
        assert len(results) == 1
        assert results[0] == [mock_repo]

    @patch(f"{MODULE}.logger")
    @patch(f"{MODULE}.gitlab.Client")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.create")
    def test_create_failure_logs_error(
        self, mock_create, mock_unique, mock_client_cls, mock_logger
    ):
        """IntegrityError on create() should call logger.error."""
        from frege.indexers.models import GitLabIndexer

        mock_create.side_effect = IntegrityError("duplicate key")

        mock_client = Mock()
        mock_client.repositories.return_value = iter([
            ({"git_url": "http://example.com/repo1.git", "name": "repo1"}, 100),
        ])
        mock_client_cls.return_value = mock_client

        indexer = GitLabIndexer()
        with patch.object(GitLabIndexer, "save"):
            list(indexer)

        mock_logger.error.assert_called_once()
        assert "http://example.com/repo1.git" in mock_logger.error.call_args[0][0]

    @patch(f"{MODULE}.gitlab.Client")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.create")
    def test_all_creates_fail_cursor_still_advances(
        self, mock_create, mock_unique, mock_client_cls
    ):
        """Even if all create() calls fail, cursor should advance to last ID."""
        from frege.indexers.models import GitLabIndexer

        mock_create.side_effect = IntegrityError("duplicate")

        mock_client = Mock()
        mock_client.repositories.return_value = iter([
            ({"git_url": "http://example.com/r1.git", "name": "r1"}, 10),
            ({"git_url": "http://example.com/r2.git", "name": "r2"}, 20),
            ({"git_url": "http://example.com/r3.git", "name": "r3"}, 30),
        ])
        mock_client_cls.return_value = mock_client

        indexer = GitLabIndexer()
        with patch.object(GitLabIndexer, "save"):
            list(indexer)

        assert indexer.last_project_id == 30


@pytest.mark.django_db
class TestBitbucketIndexerErrorHandling:
    """Tests for BitbucketIndexer.__iter__() error handling."""

    @patch(f"{MODULE}.bitbucket.get_last_commit_hash", return_value="abc123")
    @patch(f"{MODULE}.bitbucket.get_repo_url", return_value="http://bb.org/r")
    @patch(f"{MODULE}.bitbucket.get_clone_url", return_value="http://bb.org/r.git")
    @patch(f"{MODULE}.bitbucket.get_forks_count", return_value=10)
    @patch(f"{MODULE}.bitbucket.get_next_page")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.create")
    def test_saves_cursor_after_create(
        self, mock_create, mock_unique, mock_next_page,
        mock_forks, mock_clone, mock_repo_url, mock_commit
    ):
        """save(current_date) should happen AFTER successful create()."""
        from frege.indexers.models import BitbucketIndexer
        from datetime import datetime

        date1 = datetime(2020, 1, 1)
        date2 = datetime(2020, 1, 2)

        mock_next_page.side_effect = [
            ({"name": "repo1", "description": "d"}, date2),
            (None, None),
        ]

        mock_repo = Mock()
        call_order = []

        def track_create(**kwargs):
            call_order.append("create")
            return mock_repo
        mock_create.side_effect = track_create

        indexer = BitbucketIndexer()
        indexer.current_date = date1
        indexer.min_forks = 1

        with patch.object(type(indexer), "save", side_effect=lambda **kw: call_order.append("save")):
            list(indexer)

        assert "create" in call_order
        assert "save" in call_order
        assert call_order.index("create") < call_order.index("save")

    @patch(f"{MODULE}.bitbucket.get_last_commit_hash", return_value="abc123")
    @patch(f"{MODULE}.bitbucket.get_repo_url", return_value="http://bb.org/r")
    @patch(f"{MODULE}.bitbucket.get_clone_url", return_value="http://bb.org/r.git")
    @patch(f"{MODULE}.bitbucket.get_forks_count", return_value=10)
    @patch(f"{MODULE}.bitbucket.get_next_page")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.create")
    def test_create_failure_saves_cursor_and_continues(
        self, mock_create, mock_unique, mock_next_page,
        mock_forks, mock_clone, mock_repo_url, mock_commit
    ):
        """IntegrityError on create() should save cursor and continue."""
        from frege.indexers.models import BitbucketIndexer
        from datetime import datetime

        mock_repo = Mock()
        mock_create.side_effect = [IntegrityError("dup"), mock_repo]

        mock_next_page.side_effect = [
            ({"name": "r1", "description": "d"}, datetime(2020, 1, 2)),
            ({"name": "r2", "description": "d"}, datetime(2020, 1, 3)),
            (None, None),
        ]

        indexer = BitbucketIndexer()
        indexer.current_date = datetime(2020, 1, 1)
        indexer.min_forks = 1

        with patch.object(type(indexer), "save"):
            results = list(indexer)

        # Only second repo should succeed
        assert len(results) == 1
        assert results[0] == [mock_repo]

    @patch(f"{MODULE}.logger")
    @patch(f"{MODULE}.bitbucket.get_last_commit_hash", return_value="abc123")
    @patch(f"{MODULE}.bitbucket.get_repo_url", return_value="http://bb.org/r")
    @patch(f"{MODULE}.bitbucket.get_clone_url", return_value="http://bb.org/r.git")
    @patch(f"{MODULE}.bitbucket.get_forks_count", return_value=10)
    @patch(f"{MODULE}.bitbucket.get_next_page")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.create")
    def test_create_failure_logs_error(
        self, mock_create, mock_unique, mock_next_page,
        mock_forks, mock_clone, mock_repo_url, mock_commit, mock_logger
    ):
        """IntegrityError on create() should call logger.error."""
        from frege.indexers.models import BitbucketIndexer
        from datetime import datetime

        mock_create.side_effect = IntegrityError("dup")

        mock_next_page.side_effect = [
            ({"name": "r1", "description": "d"}, datetime(2020, 1, 2)),
            (None, None),
        ]

        indexer = BitbucketIndexer()
        indexer.current_date = datetime(2020, 1, 1)
        indexer.min_forks = 1

        with patch.object(type(indexer), "save"):
            list(indexer)

        mock_logger.error.assert_called_once()
        assert "http://bb.org/r.git" in mock_logger.error.call_args[0][0]

    @patch(f"{MODULE}.bitbucket.get_next_page")
    @patch(f"{MODULE}.bitbucket.get_forks_count", return_value=10)
    @patch(f"{MODULE}.bitbucket.get_clone_url", return_value="http://bb.org/r.git")
    @patch(f"{MODULE}.bitbucket.get_repo_url", return_value="http://bb.org/r")
    @patch(f"{MODULE}.bitbucket.get_last_commit_hash", return_value="abc")
    @patch(f"{MODULE}._is_repo_unique", return_value=False)
    @patch(f"{MODULE}.Repository.objects.create")
    def test_skipped_repos_dont_create(
        self, mock_create, mock_unique, mock_commit,
        mock_repo_url, mock_clone, mock_forks, mock_next_page
    ):
        """Repos filtered by _is_repo_unique should not call create()."""
        from frege.indexers.models import BitbucketIndexer
        from datetime import datetime

        mock_next_page.side_effect = [
            ({"name": "r1", "description": "d"}, datetime(2020, 1, 2)),
            (None, None),
        ]

        indexer = BitbucketIndexer()
        indexer.current_date = datetime(2020, 1, 1)
        indexer.min_forks = 1

        with patch.object(type(indexer), "save"):
            results = list(indexer)

        mock_create.assert_not_called()
        assert results == []


@pytest.mark.django_db
class TestGitHubIndexerErrorHandling:
    """Tests for GitHubIndexer.__iter__() error handling."""

    @patch(f"{MODULE}.Github")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.bulk_create")
    def test_saves_cursor_after_bulk_create(
        self, mock_bulk_create, mock_unique, mock_github_cls
    ):
        """save(current_page) should happen AFTER bulk_create()."""
        from frege.indexers.models import GitHubIndexer

        mock_github = Mock()
        mock_repo = Mock()
        mock_repo.name = "test"
        mock_repo.description = "desc"
        mock_repo.clone_url = "http://gh.com/t.git"
        mock_repo.html_url = "http://gh.com/t"
        mock_repo.default_branch = "main"
        mock_branch = Mock()
        mock_branch.commit.sha = "abc123"
        mock_repo.get_branch.return_value = mock_branch

        # First call returns repos, second raises StopIteration via empty + rate limit
        mock_github.search_repositories.side_effect = [
            [mock_repo],
            [],
        ]
        mock_github_cls.return_value = mock_github

        call_order = []
        mock_bulk_create.side_effect = lambda objs: call_order.append("bulk_create")

        indexer = GitHubIndexer.objects.create(current_page=0)

        original_save = GitHubIndexer.save
        def track_save(self, **kwargs):
            call_order.append("save")
            original_save(self, **kwargs)

        with patch.object(GitHubIndexer, "save", track_save):
            # Get first yield (the one with data)
            it = iter(indexer)
            next(it)

        assert "bulk_create" in call_order
        assert "save" in call_order
        assert call_order.index("bulk_create") < call_order.index("save")

    @patch(f"{MODULE}.Github")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.bulk_create")
    def test_bulk_create_failure_still_saves_cursor(
        self, mock_bulk_create, mock_unique, mock_github_cls
    ):
        """IntegrityError on bulk_create() should not prevent cursor save."""
        from frege.indexers.models import GitHubIndexer
        import github

        mock_github = Mock()
        mock_repo = Mock()
        mock_repo.name = "test"
        mock_repo.description = "desc"
        mock_repo.clone_url = "http://gh.com/t.git"
        mock_repo.html_url = "http://gh.com/t"
        mock_repo.default_branch = "main"
        mock_branch = Mock()
        mock_branch.commit.sha = "abc"
        mock_repo.get_branch.return_value = mock_branch

        mock_github.search_repositories.side_effect = [
            [mock_repo],
            github.RateLimitExceededException(403, "rate limit", headers={}),
        ]
        mock_github_cls.return_value = mock_github

        mock_bulk_create.side_effect = IntegrityError("dup")

        indexer = GitHubIndexer.objects.create(current_page=0)

        with patch.object(GitHubIndexer, "save"):
            results = list(indexer)

        # current_page should have advanced
        assert indexer.current_page == 1

    @patch(f"{MODULE}.logger")
    @patch(f"{MODULE}.Github")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.bulk_create")
    def test_bulk_create_failure_logs_error(
        self, mock_bulk_create, mock_unique, mock_github_cls, mock_logger
    ):
        """IntegrityError on bulk_create() should call logger.error."""
        from frege.indexers.models import GitHubIndexer
        import github

        mock_github = Mock()
        mock_repo = Mock()
        mock_repo.name = "test"
        mock_repo.description = "desc"
        mock_repo.clone_url = "http://gh.com/t.git"
        mock_repo.html_url = "http://gh.com/t"
        mock_repo.default_branch = "main"
        mock_branch = Mock()
        mock_branch.commit.sha = "abc"
        mock_repo.get_branch.return_value = mock_branch

        mock_github.search_repositories.side_effect = [
            [mock_repo],
            github.RateLimitExceededException(403, "rate limit", headers={}),
        ]
        mock_github_cls.return_value = mock_github

        mock_bulk_create.side_effect = IntegrityError("duplicate key value")

        indexer = GitHubIndexer.objects.create(current_page=0)

        with patch.object(GitHubIndexer, "save"):
            list(indexer)

        mock_logger.error.assert_called_once()
        assert "page 0" in mock_logger.error.call_args[0][0]

    @patch(f"{MODULE}.Github")
    @patch(f"{MODULE}._is_repo_unique", return_value=True)
    @patch(f"{MODULE}.Repository.objects.bulk_create")
    def test_bulk_create_failure_yields_empty_and_continues(
        self, mock_bulk_create, mock_unique, mock_github_cls
    ):
        """After bulk_create failure, should yield repos_to_process (upserted) and continue."""
        from frege.indexers.models import GitHubIndexer
        import github

        mock_github = Mock()

        mock_repo1 = Mock()
        mock_repo1.name = "r1"
        mock_repo1.description = "d"
        mock_repo1.clone_url = "http://gh.com/r1.git"
        mock_repo1.html_url = "http://gh.com/r1"
        mock_repo1.default_branch = "main"
        mock_branch1 = Mock()
        mock_branch1.commit.sha = "a1"
        mock_repo1.get_branch.return_value = mock_branch1

        mock_repo2 = Mock()
        mock_repo2.name = "r2"
        mock_repo2.description = "d"
        mock_repo2.clone_url = "http://gh.com/r2.git"
        mock_repo2.html_url = "http://gh.com/r2"
        mock_repo2.default_branch = "main"
        mock_branch2 = Mock()
        mock_branch2.commit.sha = "a2"
        mock_repo2.get_branch.return_value = mock_branch2

        mock_github.search_repositories.side_effect = [
            [mock_repo1],
            [mock_repo2],
            github.RateLimitExceededException(403, "rate limit", headers={}),
        ]
        mock_github_cls.return_value = mock_github

        # First bulk_create fails, second succeeds
        mock_bulk_create.side_effect = [IntegrityError("dup"), None]

        indexer = GitHubIndexer.objects.create(current_page=0)

        with patch.object(GitHubIndexer, "save"):
            results = list(indexer)

        # Both pages should yield (even though first had bulk_create error)
        assert len(results) == 2
        assert indexer.current_page == 2

    @patch(f"{MODULE}.Github")
    def test_rate_limit_stops_iteration(self, mock_github_cls):
        """RateLimitExceededException should break iteration and set flag."""
        from frege.indexers.models import GitHubIndexer
        import github

        mock_github = Mock()
        mock_github.search_repositories.side_effect = github.RateLimitExceededException(
            403, "rate limit", headers={}
        )
        mock_github_cls.return_value = mock_github

        indexer = GitHubIndexer.objects.create(current_page=0)

        with patch.object(GitHubIndexer, "save"):
            results = list(indexer)

        assert results == []
        assert indexer.rate_limit_exceeded is True
