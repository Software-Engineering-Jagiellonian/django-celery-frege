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


@celeryd_after_setup.connect(sender="celery@worker_profiling")
def init_worker(sender, **kwargs):
    create_repos_task.apply_async(args=())


@shared_task
def create_repos_task():
    for filename in os.listdir(settings.DOWNLOAD_PATH):
        file_path = os.path.join(settings.DOWNLOAD_PATH, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    base_commit_message = "Very interesting commit message"
    sample_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../analyzers/profiling/samples/javascript/sample.js",
        )
    )
    for i in range(0, 16):
        dir_path = os.path.join(settings.DOWNLOAD_PATH, f"mock-repo-{i}")
        os.makedirs(dir_path, exist_ok=True)
        cwd = os.getcwd()
        logger.info(f"Creating repo in {dir_path}")
        logger.info("=======================")
        logger.info("")
        try:
            os.chdir(dir_path)
            os.system("git init")
            os.system('git config --local user.name "Dummy User"')
            os.system('git config --local user.email "dummy@example.com"')
            for j in range(0, i + 1):
                filename = f"file_{j}.js"
                with (
                    open(sample_path, "r") as src,
                    open(os.path.join(dir_path, filename), "a") as dst,
                ):
                    dst.write(src.read())
                os.system(f"git add {filename}")
                os.system(f'git commit -m "{base_commit_message}"')
            commit_message = base_commit_message
            for j in range(0, i + 1):
                commit_message += f" {commit_message}"
                for k in range(0, j):
                    filename = f"file_{k}.js"
                    with (
                        open(sample_path, "r") as src,
                        open(os.path.join(dir_path, filename), "a") as dst,
                    ):
                        dst.write(src.read())
                os.system(f"git add --all")
                os.system(f'git commit -m "{commit_message}"')

            for root, dirs, files in os.walk(dir_path):
                for momo in dirs:
                    os.chown(os.path.join(root, momo), 65534, 65534)
                for momo in files:
                    os.chown(os.path.join(root, momo), 65534, 65534)
            os.chown(dir_path, 65534, 65534)

        finally:
            os.chdir(cwd)

    repos = []
    for i in range(0, 16):
        repo_name = f"mock-repo-{i}"
        repo_path = os.path.join(settings.DOWNLOAD_PATH, repo_name)
        repo = Repository.objects.create(
            name=repo_name,
            git_url=repo_path,
        )
        repos.append(repo)

    for repo in repos:
        process_repo_task.apply_async(args=(repo.pk,))

    summarize.apply_async(args=())


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
        logger.info(
            f"Total analysis duration for all repositories: {total_duration.total_seconds()} seconds"
        )
    else:
        raise ValueError(
            "Not all repositories have been analyzed yet. Cannot summarize."
        )
