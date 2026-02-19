"""
Unit tests for frege.repositories.tasks.task_crawl module.

Covers:
- _sanitize(): Redis lock with TTL, skip when persistence enabled, skip when already sanitized
- _reschedule_unanalyzed_repos(): bulk update + per-PK apply_async
- init_worker(): sanitize call, conditional crawl triggering
"""

import pytest
from unittest.mock import patch, MagicMock, call


MODULE = "frege.repositories.tasks.task_crawl"


class TestSanitize:
    """Tests for _sanitize() function."""

    @patch(f"{MODULE}.redis.StrictRedis")
    @patch(f"{MODULE}.settings")
    def test_skips_when_persistence_enabled(self, mock_settings, mock_redis_cls):
        """When REDIS_PERSISTENCE_ENABLED=True, should not connect to Redis."""
        from frege.repositories.tasks.task_crawl import _sanitize

        mock_settings.REDIS_PERSISTENCE_ENABLED = True

        _sanitize()

        mock_redis_cls.assert_not_called()

    @patch(f"{MODULE}._reschedule_unanalyzed_repos")
    @patch(f"{MODULE}._wipe_downloads_dir")
    @patch(f"{MODULE}.Lock")
    @patch(f"{MODULE}.redis.StrictRedis")
    @patch(f"{MODULE}.settings")
    def test_acquires_lock_with_ttl(
        self, mock_settings, mock_redis_cls, mock_lock_cls,
        mock_wipe, mock_reschedule
    ):
        """Lock should be created with timeout=600."""
        from frege.repositories.tasks.task_crawl import _sanitize

        mock_settings.REDIS_PERSISTENCE_ENABLED = False
        mock_settings.REDIS_HOST = "localhost"
        mock_settings.REDIS_PORT = 6379

        mock_client = MagicMock()
        mock_redis_cls.return_value = mock_client
        mock_client.get.return_value = None

        mock_lock = MagicMock()
        mock_lock.__enter__ = MagicMock(return_value=None)
        mock_lock.__exit__ = MagicMock(return_value=False)
        mock_lock_cls.return_value = mock_lock

        _sanitize()

        mock_lock_cls.assert_called_once_with(mock_client, "sanitization_lock", timeout=600)

    @patch(f"{MODULE}._reschedule_unanalyzed_repos")
    @patch(f"{MODULE}._wipe_downloads_dir")
    @patch(f"{MODULE}.Lock")
    @patch(f"{MODULE}.redis.StrictRedis")
    @patch(f"{MODULE}.settings")
    def test_skips_when_already_sanitized(
        self, mock_settings, mock_redis_cls, mock_lock_cls,
        mock_wipe, mock_reschedule
    ):
        """When has_sanitized key exists, should not call wipe or reschedule."""
        from frege.repositories.tasks.task_crawl import _sanitize

        mock_settings.REDIS_PERSISTENCE_ENABLED = False
        mock_settings.REDIS_HOST = "localhost"
        mock_settings.REDIS_PORT = 6379

        mock_client = MagicMock()
        mock_redis_cls.return_value = mock_client
        mock_client.get.return_value = b"true"

        mock_lock = MagicMock()
        mock_lock.__enter__ = MagicMock(return_value=None)
        mock_lock.__exit__ = MagicMock(return_value=False)
        mock_lock_cls.return_value = mock_lock

        _sanitize()

        mock_wipe.assert_not_called()
        mock_reschedule.assert_not_called()

    @patch(f"{MODULE}._reschedule_unanalyzed_repos")
    @patch(f"{MODULE}._wipe_downloads_dir")
    @patch(f"{MODULE}.Lock")
    @patch(f"{MODULE}.redis.StrictRedis")
    @patch(f"{MODULE}.settings")
    def test_calls_wipe_and_reschedule_in_order(
        self, mock_settings, mock_redis_cls, mock_lock_cls,
        mock_wipe, mock_reschedule
    ):
        """Should call set(has_sanitized), then _wipe, then _reschedule."""
        from frege.repositories.tasks.task_crawl import _sanitize

        mock_settings.REDIS_PERSISTENCE_ENABLED = False
        mock_settings.REDIS_HOST = "localhost"
        mock_settings.REDIS_PORT = 6379

        mock_client = MagicMock()
        mock_redis_cls.return_value = mock_client
        mock_client.get.return_value = None

        call_order = []
        mock_client.set.side_effect = lambda *a, **kw: call_order.append("set")
        mock_wipe.side_effect = lambda: call_order.append("wipe")
        mock_reschedule.side_effect = lambda: call_order.append("reschedule")

        mock_lock = MagicMock()
        mock_lock.__enter__ = MagicMock(return_value=None)
        mock_lock.__exit__ = MagicMock(return_value=False)
        mock_lock_cls.return_value = mock_lock

        _sanitize()

        assert call_order == ["set", "wipe", "reschedule"]
        mock_client.set.assert_called_once_with("has_sanitized", "true")


@pytest.mark.django_db
class TestRescheduleUnanalyzedRepos:
    """Tests for _reschedule_unanalyzed_repos() function."""

    @patch(f"{MODULE}.process_repo_task")
    def test_bulk_update_and_schedule(self, mock_task):
        """Should bulk update analysis_failed and schedule each unanalyzed repo."""
        from frege.repositories.tasks.task_crawl import _reschedule_unanalyzed_repos
        from frege.repositories.factories import RepositoryFactory

        repo1 = RepositoryFactory(analyzed=False, analysis_failed=True)
        repo2 = RepositoryFactory(analyzed=False, analysis_failed=True)

        _reschedule_unanalyzed_repos()

        # analysis_failed should be reset to False
        repo1.refresh_from_db()
        repo2.refresh_from_db()
        assert repo1.analysis_failed is False
        assert repo2.analysis_failed is False

        # apply_async called for each repo
        expected_calls = {repo1.pk, repo2.pk}
        actual_calls = {c.kwargs["args"][0] if "args" in c.kwargs else c[1]["args"][0]
                        for c in mock_task.apply_async.call_args_list}
        assert actual_calls == expected_calls

    @patch(f"{MODULE}.process_repo_task")
    def test_skips_analyzed_repos(self, mock_task):
        """Should not schedule repos with analyzed=True."""
        from frege.repositories.tasks.task_crawl import _reschedule_unanalyzed_repos
        from frege.repositories.factories import RepositoryFactory

        analyzed = RepositoryFactory(analyzed=True)
        unanalyzed = RepositoryFactory(analyzed=False)

        _reschedule_unanalyzed_repos()

        # Only one call for the unanalyzed repo
        assert mock_task.apply_async.call_count == 1
        mock_task.apply_async.assert_called_once_with(args=(unanalyzed.pk,))

    @patch(f"{MODULE}.process_repo_task")
    def test_no_repos_logs_and_returns(self, mock_task, caplog):
        """Empty database should log 'No repositories found'."""
        from frege.repositories.tasks.task_crawl import _reschedule_unanalyzed_repos

        import logging
        with caplog.at_level(logging.INFO):
            _reschedule_unanalyzed_repos()

        assert "No repositories found" in caplog.text
        mock_task.apply_async.assert_not_called()

    @patch(f"{MODULE}.logger")
    @patch(f"{MODULE}.Repository.objects")
    def test_handles_exception(self, mock_objects, mock_logger):
        """Database exception should be caught and logged, not propagated."""
        from frege.repositories.tasks.task_crawl import _reschedule_unanalyzed_repos

        mock_objects.all.side_effect = Exception("DB error")

        _reschedule_unanalyzed_repos()

        mock_logger.error.assert_called_once()
        assert "DB error" in mock_logger.error.call_args[0][0]


class TestInitWorker:
    """Tests for init_worker() signal handler."""

    @patch(f"{MODULE}.crawl_repos_task")
    @patch(f"{MODULE}._sanitize")
    def test_calls_sanitize(self, mock_sanitize, mock_crawl):
        """init_worker should always call _sanitize()."""
        from frege.repositories.tasks.task_crawl import init_worker

        with patch.dict("os.environ", {"CELERY_CRAWL_ON_STARTUP": "false"}):
            init_worker(sender="celery@worker_crawl")

        mock_sanitize.assert_called_once()

    @patch(f"{MODULE}.indexers", [type("FakeIndexer1", (), {"__name__": "FakeIndexer1"})])
    @patch(f"{MODULE}.crawl_repos_task")
    @patch(f"{MODULE}._sanitize")
    def test_triggers_crawl_when_enabled(self, mock_sanitize, mock_crawl):
        """With CELERY_CRAWL_ON_STARTUP=true, should call apply_async per indexer."""
        from frege.repositories.tasks.task_crawl import init_worker

        with patch.dict("os.environ", {"CELERY_CRAWL_ON_STARTUP": "true"}):
            init_worker(sender="celery@worker_crawl")

        mock_crawl.apply_async.assert_called_once_with(args=("FakeIndexer1",))

    @patch(f"{MODULE}.crawl_repos_task")
    @patch(f"{MODULE}._sanitize")
    def test_skips_crawl_when_disabled(self, mock_sanitize, mock_crawl):
        """With CELERY_CRAWL_ON_STARTUP=false, should not call apply_async."""
        from frege.repositories.tasks.task_crawl import init_worker

        with patch.dict("os.environ", {"CELERY_CRAWL_ON_STARTUP": "false"}):
            init_worker(sender="celery@worker_crawl")

        mock_crawl.apply_async.assert_not_called()

    @patch(f"{MODULE}.indexers", [type("FakeIndexer2", (), {"__name__": "FakeIndexer2"})])
    @patch(f"{MODULE}.crawl_repos_task")
    @patch(f"{MODULE}._sanitize")
    def test_default_crawl_is_true(self, mock_sanitize, mock_crawl):
        """Without CELERY_CRAWL_ON_STARTUP env var, should crawl by default."""
        from frege.repositories.tasks.task_crawl import init_worker

        with patch.dict("os.environ", {}, clear=True):
            init_worker(sender="celery@worker_crawl")

        mock_crawl.apply_async.assert_called_once_with(args=("FakeIndexer2",))
