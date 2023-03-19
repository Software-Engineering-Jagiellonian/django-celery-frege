import os
import shutil
from contextlib import closing
from pathlib import Path
from typing import Optional

import git
from celery import shared_task
from celery.signals import celeryd_init
from celery.utils.log import get_task_logger
from django.apps import apps
from django.db import transaction
from django.utils import timezone

from fregepoc import settings
from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.celery_app import app
from fregepoc.indexers.base import BaseIndexer, indexers
from fregepoc.repositories.exceptions import (
    DownloadDirectoryFullException,
    DownloadQueueTooBigException,
)
from fregepoc.repositories.models import Repository, RepositoryFile
from fregepoc.repositories.utils.paths import (
    get_repo_files,
    get_repo_local_path,
)

logger = get_task_logger(__name__)


def _finalize_repo_analysis(repo_obj):
    if not repo_obj.files.filter(analyzed=False).exists():
        repo_obj.analyzed = True
        repo_obj.save(update_fields=["analyzed"])
        logger.info(
            f"Repository {repo_obj.git_url} fully analyzed, attempting delete"
        )
        repo_local_path = get_repo_local_path(repo_obj)
        shutil.rmtree(str(repo_local_path), ignore_errors=True)
        logger.info(
            f"Repository {repo_obj.git_url} files deleted successfully"
        )


def _delete_file(path: Path, repo: str):
    logger.info(f"Deleting file {path} for repository {repo}")
    path.unlink(missing_ok=True)
    logger.info(f"File {path} deleted for repository {repo}")


def _clone_repo(repo: Repository, local_path: Path) -> Optional[git.Repo]:
    try:
        repo_obj = git.Repo.clone_from(repo.git_url, local_path)
        repo.fetch_time = timezone.now()
        repo.save(update_fields=["fetch_time"])
        logger.info(f"Repository {repo.git_url} cloned")
        return repo_obj
    except git.exc.GitCommandError:
        try:
            repo_obj = git.Repo(local_path)
            logger.info(
                f"Repo {repo.git_url} already exists, fetched from disk"
            )
            return repo_obj
        except git.exc.NoSuchPathError:
            logger.error(
                "Tried fetching from disk, but repository does not exist"
            )
            return None


def _check_download_folder_size():
    """
    Check if the size of downloads folder < DOWNLOAD_DIR_MAX_SIZE_BYTES.
    If not, raise DownloadDirectoryFullException
    """
    path = Path(settings.DOWNLOAD_PATH)
    files = list(
        path.glob("**/*")
    )  # This is necessary because files can get deleted while being processed
    size = sum(f.stat().st_size for f in files if f.exists() and f.is_file())
    logger.info(f"Current temp file size = {size}")
    if size >= settings.DOWNLOAD_DIR_MAX_SIZE_BYTES:
        raise DownloadDirectoryFullException(
            f"Current temp file too big. Size = {size}"
        )


def _check_queued_tasks_number():
    """
    Check the number of currently registered download tasks
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


@celeryd_init.connect
def init_worker(**kwargs):
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
    default_retry_delay=5,
)
def crawl_repos_task(indexer_class_name):
    try:
        _check_queued_tasks_number()
    except DownloadQueueTooBigException as ex:
        # Trigger Celery auto retry by re-raising exception
        logger.info("Download queue too big. Retrying")
        raise ex
    except ValueError:
        logger.info("Failed to inspect queue")

    try:
        _check_download_folder_size()
    except DownloadDirectoryFullException as ex:
        # Trigger Celery auto retry by re-raising exception
        logger.info("Too many files downloaded currently. Retrying")
        raise ex

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
    for repo in batch:
        repo.refresh_from_db()
        if not repo.analyzed:
            process_repo_task.apply_async(args=(repo.pk,))


@shared_task
def process_repo_task(repo_pk):
    # TODO: docstring & cleanup

    try:
        repo = Repository.objects.get(pk=repo_pk)
    except Repository.DoesNotExist:
        logger.error(f"Repository does not exist ({repo_pk = })")
        return

    repo_local_path = get_repo_local_path(repo)

    if repo_local_path is None:
        logger.info(f"repo_local_path for {repo.git_url} is None. Aborting.")
        return

    logger.info(f"Fetching repository via url: {repo.git_url}")
    repo_obj = _clone_repo(repo, repo_local_path)
    if repo_obj is None:
        return

    with closing(repo_obj) as cloned_repo:
        repo_path = get_repo_local_path(repo)
        files = []
        for relative_file_path, language in get_repo_files(cloned_repo):
            absolute_file_path = repo_path / relative_file_path

            if not AnalyzerFactory.has_analyzers(language):
                _delete_file(absolute_file_path, repo.name)
            else:
                file = RepositoryFile(
                    repository=repo,
                    repo_relative_file_path=relative_file_path,
                    language=language,
                    analyzed=False,
                )
                files.append(file)

        RepositoryFile.objects.bulk_create(files)

    for repo_file in files:
        analyze_file_task.apply_async(args=(repo_file.pk,))

    _finalize_repo_analysis(repo)


@shared_task
def analyze_file_task(repo_file_pk):
    # TODO: docstring & cleanup

    try:
        repo_file = RepositoryFile.objects.get(pk=repo_file_pk)
    except RepositoryFile.DoesNotExist:
        logger.error(f"repo_file for pk {repo_file_pk} does not exist")
        return

    analyzers = AnalyzerFactory.make_analyzers(repo_file.language)
    if not analyzers:
        repository = repo_file.repository
        repo_file.delete()
        _finalize_repo_analysis(repository)
        return

    metrics_dict = {}
    for analyzer in analyzers:
        try:
            metrics_dict |= analyzer.analyze(repo_file)
        except Exception:
            # This should use more specific exception but some analyzer is
            # raising undocumented exceptions
            logger.error(
                f"Failed to analyze {repo_file.repository.git_url} for "
                f"analyzer {analyzer}"
            )

    with transaction.atomic():
        repo_file.metrics = metrics_dict
        repo_file.analyzed = True
        repo_file.analyzed_time = timezone.now()
        repo_file.save(update_fields=["metrics", "analyzed", "analyzed_time"])

    logger.info(f"repo_file {repo_file.repository.git_url} analyzed")

    absolute_file_path = (
        get_repo_local_path(repo_file.repository)
        / repo_file.repo_relative_file_path
    )
    _delete_file(Path(absolute_file_path), repo_file.repository.name)

    _finalize_repo_analysis(repo_file.repository)
