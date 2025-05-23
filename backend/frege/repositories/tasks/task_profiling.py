import os
import shutil

from celery import shared_task
from celery.signals import celeryd_after_setup
from celery.utils.log import get_task_logger

from frege import settings
from frege.repositories.models import (
    Repository,
)
from .task_repo import process_repo_task

logger = get_task_logger(__name__)


@shared_task
def create_repos_task():
    for filename in os.listdir(settings.DOWNLOAD_PATH):
        file_path = os.path.join(settings.DOWNLOAD_PATH, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    repos = []
    bundles_path = os.path.join(os.path.dirname(__file__), "../bundles")

    for bundle in os.listdir(bundles_path):
        bundle_path = os.path.abspath(os.path.join(bundles_path, bundle))
        bundle_basename = os.path.basename(bundle)
        repo = Repository.objects.create(
            name=bundle_basename,
            git_url=bundle_path,
        )
        repos.append(repo)

    for repo in repos:
        process_repo_task.apply_async(args=(repo.pk,))

    summarize_task = summarize.apply_async(args=())
    return summarize_task.id


@shared_task(
    autoretry_for=(ValueError,),
    max_retries=None,
    default_retry_delay=5,
)
def summarize():
    if Repository.objects.exists() and all(
        repo.analyzed for repo in Repository.objects.all()
    ):

        repos = Repository.objects.all()

        repos = repos.order_by("pk")

        earliest_fetch_time = min(repo.fetch_time for repo in repos)
        latest_analyzed_time = max(repo.analyzed_time for repo in repos)
        total_duration = latest_analyzed_time - earliest_fetch_time
        return f"Total analysis duration for all repositories: {total_duration.total_seconds()} seconds"
    else:
        raise ValueError(
            "Not all repositories have been analyzed yet. Cannot summarize."
        )
