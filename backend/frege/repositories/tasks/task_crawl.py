import os
import shutil

from celery import shared_task
from celery.signals import celeryd_after_setup
from celery.utils.log import get_task_logger
from django.apps import apps

from frege import settings
from frege.celery_app import app
from frege.indexers.base import BaseIndexer, indexers
from frege.repositories.exceptions import (
    DownloadDirectoryFullException,
    DownloadQueueTooBigException,
)
from frege.repositories.models import (
    Repository,
)
import redis
from redis.lock import Lock
from .task_repo import process_repo_task

logger = get_task_logger(__name__)


@celeryd_after_setup.connect(sender="celery@worker_crawl")
def init_worker(sender, **kwargs):
    """
    Initializes worker on startup.

    Triggers the crawling task for each indexer if CELERY_CRAWL_ON_STARTUP is true.
    """
    _sanitize()

    if os.environ.get("CELERY_CRAWL_ON_STARTUP", "true").lower() != "true":
        return

    for indexer_cls in indexers:
        crawl_repos_task.apply_async(args=(indexer_cls.__name__,))


@shared_task(
    autoretry_for=[
        DownloadDirectoryFullException,
        DownloadQueueTooBigException,
    ],
    max_retries=None,
    default_retry_delay=15,
)
def crawl_repos_task(indexer_class_name):
    """
    Main crawling task that schedules repository processing.

    Args:
        indexer_class_name (str): The name of the indexer class used to fetch repositories.

    Raises:
        DownloadDirectoryFullException: If the download folder is full.
        DownloadQueueTooBigException: If the task queue is too long.
    """
    try:
        _check_queued_tasks_number()
    except DownloadQueueTooBigException as ex:
        # Trigger Celery auto retry by re-raising exception
        logger.info("Download queue too big. Retrying")
        raise ex
    except ValueError as ex:
        logger.info(f"Failed to inspect queue with exception {ex}")

    indexer_model = apps.get_model("indexers", indexer_class_name)
    indexer: BaseIndexer = indexer_model.load()

    if indexer.rate_limit_exceeded:
        logger.info(
            f"The rate limit has been exceeded for "
            f"{indexer.__class__.__qualname__}. "
            f"Waiting {indexer.rate_limit_timeout}"
        )
        crawl_repos_task.apply_async(
            args=(indexer_class_name,),
            countdown=indexer.rate_limit_timeout.seconds,
        )
        return

    crawl_repos_task.apply_async(args=(indexer_class_name,))

    batch = next(iter(indexer), [])
    logger.info(f"Scheduling batch of {len(batch)} repositories")
    for repo in batch:
        repo.refresh_from_db()
        if not repo.analyzed and not repo.analysis_failed:
            process_repo_task.apply_async(args=(repo.pk,))


def _sanitize():
    """
    Sanitizes the environment before crawling new repositories.

    If Redis-based task persistence is disabled, this function:
    - Acquires a lock to ensure a single crawler performs sanitization.
    - Wipes the downloads directory.
    - Reschedules all unanalyzed repositories for processing.
    """
    if settings.REDIS_PERSISTENCE_ENABLED:
        # If persistence is enabled, we don't need to sanitize
        # since all previous tasks are still in the queue.
        return
    client = redis.StrictRedis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT
    )
    lock = Lock(client, "sanitization_lock", timeout=600)
    with lock:
        # Wait for only one crawler to sanitize. We cannot safely clean
        # the download dir and reschedule unanalyzed repos concurrently.
        has_sanitized = client.get("has_sanitized")
        if has_sanitized is not None:
            return
        client.set("has_sanitized", "true")
        logger.info("Sanitizing")
        _wipe_downloads_dir()
        _reschedule_unanalyzed_repos()


def _wipe_downloads_dir():
    """
    Deletes all contents of the downloads directory.

    Used to clear previously cloned repository files from local storage.
    """
    for filename in os.listdir(settings.DOWNLOAD_PATH):
        file_path = os.path.join(settings.DOWNLOAD_PATH, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def _reschedule_unanalyzed_repos():
    """
    Reschedules analysis tasks for repositories that haven't been analyzed yet.

    This is used after wiping the download directory to reprocess incomplete repositories.
    Logs the number of rescheduled repositories or if none are found.
    """
    try:
        objects = Repository.objects.all()
        if objects.exists():
            unanalyzed_repos = Repository.objects.filter(analyzed=False)
            logger.info(
                f"Rescheduling {unanalyzed_repos.count()} unanalyzed repositories"
            )
            unanalyzed_repos.update(analysis_failed=False)
            for repo_pk in unanalyzed_repos.values_list("pk", flat=True).iterator(chunk_size=1000):
                process_repo_task.apply_async(args=(repo_pk,))
        else:
            logger.info("No repositories found")
            return
    except Exception as ex:
        logger.error(f"Failed to reschedule unanalyzed repositories: {ex}")


def _check_queued_tasks_number():
    """
    Checks how many download tasks are currently queued for execution.

    Raises:
        DownloadQueueTooBigException: If the number of reserved tasks exceeds the limit.
        ValueError: If inspection of the queue fails.
    """
    name = settings.DOWNLOAD_TASK_NAME
    inspect = app.control.inspect([name])

    if inspect is None:
        raise ValueError(f"Failed to inspect worker {name}")

    reserved_dict = inspect.reserved()

    if reserved_dict is None:
        raise ValueError("Failed to get reserved tasks")

    reserved = len(reserved_dict[name])
    logger.info(f"Currently reserved tasks {reserved}")

    if reserved > settings.MAX_DOWNLOAD_TASKS_COUNT:
        raise DownloadQueueTooBigException(count=reserved)
