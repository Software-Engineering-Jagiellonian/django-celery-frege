from contextlib import closing
from pathlib import Path
from typing import Optional

import git
from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from .task_commit import (
    analyze_commit_message_quality_task,
)
from .task_file import analyze_file_task
from frege import settings
from frege.analyzers.core import AnalyzerFactory
from frege.repositories.exceptions import (
    DownloadDirectoryFullException,
)
from frege.repositories.models import (
    Repository,
    RepositoryFile,
    CommitMessage,
    RepositoryCommitMessagesQuality,
)
from frege.repositories.utils.paths import (
    get_repo_files,
    get_repo_local_path,
)
from .common import finalize_repo_analysis

logger = get_task_logger(__name__)


@shared_task(
    autoretry_for=[
        DownloadDirectoryFullException,
    ],
    max_retries=None,
    default_retry_delay=15,
)
def process_repo_task(repo_pk):
    # TODO: docstring & cleanup

    try:
        repo = Repository.objects.get(pk=repo_pk)
    except Repository.DoesNotExist:
        logger.error(f"Repository does not exist ({repo_pk = })")
        return

    logger.info(f"Processing repository {repo.git_url}")

    _remove_database_entries(repo)

    repo_local_path = get_repo_local_path(repo)

    if repo_local_path is None:
        logger.info(f"repo_local_path for {repo.git_url} is None. Aborting.")
        return

    logger.info(f"Fetching repository via url: {repo.git_url}")
    repo_obj = _clone_repo(repo, repo_local_path)
    if repo_obj is None:
        if not repo.analysis_failed:
            error_message = f"Failed to obtain repository {repo.git_url}. This has unknown consequences."
        else:
            error_message = (
                f"Repository {repo.git_url} marked as failed. Skipping."
            )

        logger.error(error_message)

        return

    with closing(repo_obj) as cloned_repo:
        repo_path = get_repo_local_path(repo)
        files = []
        all_commit_messages = []

        commits = []
        for head in cloned_repo.heads:
            commits.extend(list(cloned_repo.iter_commits(head)))
        commits = list(set(commits))

        for commit in commits:
            commit_message = CommitMessage(
                repository=repo,
                author=commit.author.name,
                message=commit.message,
                commit_hash=commit.hexsha,
                analyzed=False,
            )
            all_commit_messages.append(commit_message)

        # Not limiting batch sizes can lead to OutOfMemory exceptions
        # for the database when handling large repositories.
        batch_size = 128
        for i in range(0, len(all_commit_messages), batch_size):
            CommitMessage.objects.bulk_create(
                all_commit_messages[i : i + batch_size]
            )

        repo_quality_metrics = RepositoryCommitMessagesQuality(
            repository=repo, analyzed=False
        )
        repo_quality_metrics.save()

        for relative_file_path, language in get_repo_files(cloned_repo):
            if not AnalyzerFactory.has_analyzers(language):
                continue

            file = RepositoryFile(
                repository=repo,
                repo_relative_file_path=relative_file_path,
                language=language,
                analyzed=False,
            )
            files.append(file)
        RepositoryFile.objects.bulk_create(files)

        for commit_message in all_commit_messages:
            analyze_commit_message_quality_task.apply_async(
                args=(commit_message.pk,)
            )

        for repo_file in files:
            analyze_file_task.apply_async(args=(repo_file.pk,))

    finalize_repo_analysis(repo)


def _clone_repo(repo: Repository, local_path: Path) -> Optional[git.Repo]:
    _check_download_folder_size()

    try:
        repo_obj = git.Repo.clone_from(repo.git_url, local_path)
        repo.fetch_time = timezone.now()
        repo.save(update_fields=["fetch_time"])
        logger.info(f"Repository {repo.git_url} cloned")
        return repo_obj
    except Exception as e:
        logger.error(
            f"Unexpected error while processing repository {repo.git_url}: {e}"
        )
        repo.analysis_failed = True
        repo.save(update_fields=["analysis_failed"])

        return None


def _check_download_folder_size(depth=0):
    """
    Check if the size of downloads folder < DOWNLOAD_DIR_MAX_SIZE_BYTES.
    If not, raise DownloadDirectoryFullException
    """
    if depth > 7:
        # Prevent infinite recursion
        logger.error("Failed to check download folder size.")
        raise DownloadDirectoryFullException(
            f"Couldn't determine download folder size after {depth} attempts."
        )
    path = Path(settings.DOWNLOAD_PATH)
    try:
        files = list(
            path.glob("**/*")
        )  # This is necessary because files can get deleted while being processed
        size = sum(
            f.stat().st_size for f in files if f.exists() and f.is_file()
        )
        logger.info(f"Current temp file size = {size}")
        if size >= settings.DOWNLOAD_DIR_MAX_SIZE_BYTES:
            raise DownloadDirectoryFullException(
                f"Current temp file too big. Size = {size}"
            )
    except FileNotFoundError:
        logger.warning(
            "Directory in download folder not found. Retrying the check of download folder size."
        )
        _check_download_folder_size(depth + 1)


def _remove_database_entries(repo: Repository):
    """
    When processing a repository we need to make sure to remove all previous database entries, because we insert into the database all the files and commit messages again.
    """
    repo_pk = repo.pk
    removed_commits_amount = CommitMessage.objects.filter(
        repository=repo_pk
    ).delete()[0]
    removed_repo_quality_metrics_amount = (
        RepositoryCommitMessagesQuality.objects.filter(
            repository=repo_pk
        ).delete()[0]
    )
    removed_files_amount = RepositoryFile.objects.filter(
        repository=repo_pk
    ).delete()[0]

    if (
        removed_commits_amount > 0
        or removed_repo_quality_metrics_amount > 0
        or removed_files_amount > 0
    ):
        logger.warning(
            f"Had to remove database entries for repository \"{repo.name}\". This shouldn't happen unless you're restarting FREGE and rescheduling unanalyzed repos."
        )
    repo.analyzed = False
    repo.save(update_fields=["analyzed"])
