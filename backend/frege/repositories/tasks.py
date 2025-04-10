import os
import shutil
from contextlib import closing
from pathlib import Path
from typing import Optional

import git
from celery import shared_task
from celery.signals import celeryd_after_setup
from celery.utils.log import get_task_logger
from django.apps import apps
from django.db import transaction
from django.utils import timezone

from frege import settings
from frege.analyzers.core import AnalyzerFactory
from frege.celery_app import app
from frege.indexers.base import BaseIndexer, indexers
from frege.repositories.commit_messages import CommitMessagesQualityRepoAnalyzer, CommitMessageAnalyzer
from frege.repositories.exceptions import (
    DownloadDirectoryFullException,
    DownloadQueueTooBigException,
)
from frege.repositories.models import Repository, RepositoryFile, CommitMessage, RepositoryCommitMessagesQuality
from frege.repositories.utils.paths import (
    get_repo_files,
    get_repo_local_path,
)
import redis
from redis.lock import Lock

logger = get_task_logger(__name__)


def _finalize_repo_analysis(repo_obj):
    if not (
            repo_obj.files.filter(analyzed=False).exists() or
            repo_obj.commit_messages.filter(analyzed=False).exists()
    ):
        logger.info(f"Repository {repo_obj.git_url} commit messages quality calculation")
        repo_quality_metrics = RepositoryCommitMessagesQuality.objects.get(repository=repo_obj)
        commit_messages = CommitMessage.objects.filter(repository=repo_obj.pk)
        analyzer = CommitMessagesQualityRepoAnalyzer(commit_messages)

        with transaction.atomic():
            repo_quality_metrics.analyzed = True
            repo_quality_metrics.commits_amount = analyzer.commits_amount
            repo_quality_metrics.average_commit_message_characters_length = analyzer.average_commit_message_length
            repo_quality_metrics.average_commit_message_words_amount = analyzer.average_commit_message_words_amount
            repo_quality_metrics.average_commit_message_fog_index = analyzer.average_commit_message_fog_index
            repo_quality_metrics.classifiable_to_unclassifiable_commit_messages_ratio = analyzer.classified_to_unclassified_cm_ratio
            repo_quality_metrics.percentage_of_feature_commits = analyzer.percentage_of_feature_commits
            repo_quality_metrics.percentage_of_fix_commits = analyzer.percentage_of_fix_commits
            repo_quality_metrics.percentage_of_config_change_commits = analyzer.percentage_of_config_change_commits
            repo_quality_metrics.percentage_of_merge_pr_commits = analyzer.percentage_of_merge_pr_commits
            repo_quality_metrics.percentage_of_unclassified_commits = analyzer.percentage_of_unclassified_commits

            repo_quality_metrics.save(update_fields=[
                "analyzed",
                "commits_amount",
                "average_commit_message_characters_length",
                "average_commit_message_words_amount",
                "average_commit_message_fog_index",
                "classifiable_to_unclassifiable_commit_messages_ratio",
                "percentage_of_feature_commits",
                "percentage_of_fix_commits",
                "percentage_of_config_change_commits",
                "percentage_of_merge_pr_commits",
                "percentage_of_unclassified_commits"
            ])
            logger.info(f"Repository {repo_obj.git_url} commit messages quality calculation finished successfully!")

        with transaction.atomic():
            repo_obj.analyzed = True
            repo_obj.analyzed_time = timezone.now()
            repo_obj.save(update_fields=["analyzed", "analyzed_time", ])

        logger.info(f"Repository {repo_obj.git_url} fully analyzed, attempting delete")

        repo_local_path = get_repo_local_path(repo_obj)
        shutil.rmtree(str(repo_local_path), ignore_errors=True)

        logger.info(f"Repository {repo_obj.git_url} files deleted successfully")

def _clone_repo(repo: Repository, local_path: Path) -> Optional[git.Repo]:
    _check_download_folder_size()

    try:
        repo_obj = git.Repo.clone_from(repo.git_url, local_path)
        repo.fetch_time = timezone.now()
        repo.save(update_fields=["fetch_time"])
        logger.info(f"Repository {repo.git_url} cloned")
        return repo_obj
    except git.exc.GitCommandError as e:
        logger.error(f"Git error while cloning repository {repo.git_url}.")
    except Exception as e:
        logger.error(f"Unexpected error while processing repository {repo.git_url}: {e}")
        
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
        size = sum(f.stat().st_size for f in files if f.exists() and f.is_file())
        logger.info(f"Current temp file size = {size}")
        if size >= settings.DOWNLOAD_DIR_MAX_SIZE_BYTES:
            raise DownloadDirectoryFullException(
                f"Current temp file too big. Size = {size}"
            )
    except FileNotFoundError:
        logger.warning("Directory in download folder not found. Retrying the check of download folder size.")
        _check_download_folder_size(depth+1)

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

@celeryd_after_setup.connect(sender="celery@worker_crawl")
def init_worker(sender, **kwargs):
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
    
    if repo.analysis_failed:
        logger.info(f"Repository {repo.git_url} marked as failed. Skipping processing.")
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
            error_message = f"Repository {repo.git_url} marked as failed. Skipping."
            
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
                analyzed=False
            )
            all_commit_messages.append(commit_message)

        # Not limiting batch sizes can lead to OutOfMemory exceptions
        # for the database when handling large repositories.
        batch_size = 128
        for i in range(0, len(all_commit_messages), batch_size):
            CommitMessage.objects.bulk_create(all_commit_messages[i:i + batch_size])

        repo_quality_metrics = RepositoryCommitMessagesQuality(repository=repo, analyzed=False)
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
            analyze_commit_message_quality_task.apply_async(args=(commit_message.pk,))

        for repo_file in files:
            analyze_file_task.apply_async(args=(repo_file.pk,))

    _finalize_repo_analysis(repo)

@shared_task
def analyze_commit_message_quality_task(commit_message_pk):
    try:
        logger.info(f"Attempt of analyzing commit message {commit_message_pk} quality")
        commit_message = CommitMessage.objects.get(pk=commit_message_pk)
    except CommitMessage.DoesNotExist:
        logger.error(f"commit message for pk {commit_message_pk} does not exist")
        return

    try:
        analyzed_commit_message = CommitMessageAnalyzer(commit_message.message)

        with transaction.atomic():
            commit_message.commit_type = analyzed_commit_message.commit_type
            commit_message.commit_message_char_length = analyzed_commit_message.message_length
            commit_message.words_amount = analyzed_commit_message.words_amount
            commit_message.average_word_length = analyzed_commit_message.average_words_length
            commit_message.fog_index = analyzed_commit_message.fog_index
            commit_message.analyzed = True
            commit_message.analyzed_time = timezone.now()
            commit_message.save(update_fields=["analyzed", "analyzed_time", "commit_type", "fog_index",
                                               "commit_message_char_length", "words_amount", "average_word_length"])
    except Exception as error:
        with transaction.atomic():
            commit_message.analyzed = True
            commit_message.analyzed_time = timezone.now()
            commit_message.save(update_fields=["analyzed", "analyzed_time"])
        logger.error(f"Can't analyze commit message {commit_message.message}")
        logger.error(error, exc_info=True)
    finally:
        logger.info(f"commit_message {commit_message.commit_hash} "
                    f"from repository {commit_message.repository.name} analyzed successfully!")
        _finalize_repo_analysis(commit_message.repository)

@shared_task
def analyze_file_task(repo_file_pk):
    try:
        repo_file = RepositoryFile.objects.get(pk=repo_file_pk)
    except RepositoryFile.DoesNotExist:
        logger.error(f"repo_file for pk {repo_file_pk} does not exist")
        return

    file_failed = False

    try:
        analyzers = AnalyzerFactory.make_analyzers(repo_file.language)
        if not analyzers:
            logger.warning(f"No analyzers for language {repo_file.language}, deleting file")
            repository = repo_file.repository
            repo_file.delete()
            _finalize_repo_analysis(repository)
            return {"status": "skipped", "reason": "no analyzers"}

        metrics_dict = {}
        for analyzer in analyzers:
            try:
                metrics_dict |= analyzer.analyze(repo_file)
            except Exception as e:
                logger.warning(
                    f"Analyzer {analyzer} failed for file {repo_file.repo_relative_file_path}: {e}"
                )
                file_failed = True

        with transaction.atomic():
            repo_file.metrics = metrics_dict
            repo_file.analyzed = True
            repo_file.analyzed_time = timezone.now()
            repo_file.analysis_failed = file_failed
            repo_file.lines_of_code = metrics_dict.get("lines_of_code", 0)
            repo_file.token_count = metrics_dict.get("token_count", 0)
            repo_file.function_count = metrics_dict.get("function_count", 0)
            repo_file.average_function_name_length = metrics_dict.get("average_function_name_length", 0)
            repo_file.average_lines_of_code = metrics_dict.get("average_lines_of_code", 0)
            repo_file.average_token_count = metrics_dict.get("average_token_count", 0)
            repo_file.average_cyclomatic_complexity = metrics_dict.get("average_cyclomatic_complexity", 0)
            repo_file.average_parameter_count = metrics_dict.get("average_parameter_count", 0)

            repo_file.save(update_fields=[
                "metrics",
                "analyzed",
                "analyzed_time",
                "analysis_failed",
                "lines_of_code",
                "token_count",
                "function_count",
                "average_function_name_length",
                "average_lines_of_code",
                "average_token_count",
                "average_cyclomatic_complexity",
                "average_parameter_count"
            ])

        logger.info(f"File {repo_file.repo_relative_file_path} analyzed (failed={file_failed})")

    except Exception as error:
        repo_file.analyzed = True
        repo_file.analysis_failed = True
        repo_file.save(update_fields=["analyzed", "analysis_failed"])

        logger.error(f"Unexpected error during analysis of file {repo_file.repo_relative_file_path}", exc_info=True)

    finally:
        absolute_file_path = (
                get_repo_local_path(repo_file.repository)
                / repo_file.repo_relative_file_path
        )

        _finalize_repo_analysis(repo_file.repository)

def _remove_database_entries(repo: Repository):
    """
    When processing a repository we need to make sure to remove all previous database entries, because we insert into the database all the files and commit messages again.
    """
    repo_pk = repo.pk
    removed_commits_amount = CommitMessage.objects.filter(repository=repo_pk).delete()[0]
    removed_repo_quality_metrics_amount = RepositoryCommitMessagesQuality.objects.filter(repository=repo_pk).delete()[0]
    removed_files_amount = RepositoryFile.objects.filter(repository=repo_pk).delete()[0]

    if(removed_commits_amount > 0 or removed_repo_quality_metrics_amount > 0 or removed_files_amount > 0):
        logger.warning(f"Had to remove database entries for repository \"{repo.name}\". This shouldn't happen unless you're restarting FREGE and rescheduling unanalyzed repos.")
    repo.analyzed = False
    repo.save(update_fields=["analyzed"])

def _sanitize():
    if settings.REDIS_PERSISTENCE_ENABLED:
        # If persistence is enabled, we don't need to sanitize
        # since all previous tasks are still in the queue.
        return
    client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    lock = Lock(client, "sanitization_lock")
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
    for filename in os.listdir(settings.DOWNLOAD_PATH):
        file_path = os.path.join(settings.DOWNLOAD_PATH, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def _reschedule_unanalyzed_repos():
    try:
        objects = Repository.objects.all()
        if objects.exists():
            unanalyzed_repos = Repository.objects.filter(analyzed=False)
            logger.info(f"Rescheduling {unanalyzed_repos.count()} unanalyzed repositories")
            for repo in unanalyzed_repos:
                repo.analysis_failed = False
                repo.save(update_fields=["analysis_failed"])
                process_repo_task.apply_async(args=(repo.pk,))
        else:
            logger.info("No repositories found")
            return
    except Exception as ex:
        logger.error(f"Failed to reschedule unanalyzed repositories: {ex}")
