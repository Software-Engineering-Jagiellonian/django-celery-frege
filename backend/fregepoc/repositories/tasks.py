import os
from contextlib import closing
from typing import Optional

import git
from celery import shared_task
from celery.signals import celeryd_init
from celery.utils.log import get_task_logger
from django.apps import apps
from django.db import transaction
from django.utils import timezone

from fregepoc.indexers.base import BaseIndexer, indexers
from fregepoc.repositories.analyzers.base import AnalyzerFactory
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
            f"Repository {repo_obj.git_url} fully analyzed, "
            "deleting files from disk..."
        )
        repo_local_path = get_repo_local_path(repo_obj)
        os.system(f"rm -rf {repo_local_path}")


def _clone_repo(repo: Repository, local_path: str) -> Optional[git.Repo]:
    try:
        repo_obj = git.Repo.clone_from(repo.git_url, local_path)
        repo.fetch_time = timezone.now()
        repo.save(update_fields=["fetch_time"])
        logger.info("Repository cloned")
        return repo_obj
    except git.exc.GitCommandError:
        try:
            repo_obj = git.Repo(local_path)
            logger.info("Repo already exists, fetched from disk")
            return repo_obj
        except git.exc.NoSuchPathError:
            logger.error(
                "Tried fetching from disk, but repository does not exist"
            )
            return None


@celeryd_init.connect
def init_worker(**kwargs):
    if os.environ.get("CELERY_CRAWL_ON_STARTUP", "true").lower() != "true":
        return

    for indexer_cls in indexers:
        crawl_repos_task.apply_async(args=(indexer_cls.__name__,))


@shared_task
def crawl_repos_task(indexer_class_name):
    indexer_model = apps.get_model("indexers", indexer_class_name)
    indexer: BaseIndexer = indexer_model.load()

    batch = next(iter(indexer), [])
    for repo in batch:
        repo.refresh_from_db()
        if not repo.analyzed:
            process_repo_task.apply_async(args=(repo.pk,))

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
    else:
        crawl_repos_task.apply_async(args=(indexer_class_name,))


@shared_task
def process_repo_task(repo_pk):
    # TODO: docstring & cleanup

    try:
        repo = Repository.objects.get(pk=repo_pk)
    except Repository.DoesNotExist:
        logger.error(f"Repository does not exist ({repo_pk = })")
        return

    repo_local_path = get_repo_local_path(repo)
    logger.info(f"Fetching repository via url: {repo.git_url}")

    repo_obj = _clone_repo(repo, repo_local_path)
    if repo_obj is None:
        return

    with closing(repo_obj) as cloned_repo:
        repo_files = [
            RepositoryFile(
                repository=repo,
                repo_relative_file_path=relative_file_path,
                language=language,
                analyzed=False,
            )
            for relative_file_path, language in get_repo_files(cloned_repo)
            if AnalyzerFactory.has_analyzers(language)
        ]
        RepositoryFile.objects.bulk_create(repo_files)

        for repo_file in repo_files:
            analyze_file_task.apply_async(args=(repo_file.pk,))

        _finalize_repo_analysis(repo)


@shared_task
def analyze_file_task(repo_file_pk):
    # TODO: docstring & cleanup

    try:
        repo_file = RepositoryFile.objects.get(pk=repo_file_pk)
    except RepositoryFile.DoesNotExist:
        logger.error("repo_file does not exist")
        return

    analyzers = AnalyzerFactory.make_analyzers(repo_file.language)
    if not analyzers:
        repo_file.delete()
        return

    metrics_dict = {}
    for analyzer in analyzers:
        metrics_dict |= analyzer.analyze(repo_file)

    with transaction.atomic():
        repo_file.metrics = metrics_dict
        repo_file.analyzed = True
        repo_file.analyzed_time = timezone.now()
        repo_file.save(update_fields=["metrics", "analyzed", "analyzed_time"])

    logger.info(f"repo_file {repo_file.repository.name} analyzed")
    _finalize_repo_analysis(repo_file.repository)
