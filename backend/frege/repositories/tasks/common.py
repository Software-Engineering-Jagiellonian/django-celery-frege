import shutil

from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone

from frege.repositories.commit_messages import (
    CommitMessagesQualityRepoAnalyzer,
)
from frege.repositories.models import (
    CommitMessage,
    RepositoryCommitMessagesQuality,
)
from frege.repositories.utils.paths import (
    get_repo_local_path,
)

logger = get_task_logger(__name__)


def finalize_repo_analysis(repo_obj):
    if not (
        repo_obj.files.filter(analyzed=False).exists()
        or repo_obj.commit_messages.filter(analyzed=False).exists()
    ):
        logger.info(
            f"Repository {repo_obj.git_url} commit messages quality calculation"
        )
        repo_quality_metrics = RepositoryCommitMessagesQuality.objects.get(
            repository=repo_obj
        )
        commit_messages = CommitMessage.objects.filter(repository=repo_obj.pk)
        analyzer = CommitMessagesQualityRepoAnalyzer(commit_messages)

        with transaction.atomic():
            repo_quality_metrics.analyzed = True
            repo_quality_metrics.commits_amount = analyzer.commits_amount
            repo_quality_metrics.average_commit_message_characters_length = (
                analyzer.average_commit_message_length
            )
            repo_quality_metrics.average_commit_message_words_amount = (
                analyzer.average_commit_message_words_amount
            )
            repo_quality_metrics.average_commit_message_fog_index = (
                analyzer.average_commit_message_fog_index
            )
            repo_quality_metrics.classifiable_to_unclassifiable_commit_messages_ratio = (
                analyzer.classified_to_unclassified_cm_ratio
            )
            repo_quality_metrics.percentage_of_feature_commits = (
                analyzer.percentage_of_feature_commits
            )
            repo_quality_metrics.percentage_of_fix_commits = (
                analyzer.percentage_of_fix_commits
            )
            repo_quality_metrics.percentage_of_config_change_commits = (
                analyzer.percentage_of_config_change_commits
            )
            repo_quality_metrics.percentage_of_merge_pr_commits = (
                analyzer.percentage_of_merge_pr_commits
            )
            repo_quality_metrics.percentage_of_unclassified_commits = (
                analyzer.percentage_of_unclassified_commits
            )

            repo_quality_metrics.save(
                update_fields=[
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
                    "percentage_of_unclassified_commits",
                ]
            )
            logger.info(
                f"Repository {repo_obj.git_url} commit messages quality calculation finished successfully!"
            )

        with transaction.atomic():
            repo_obj.analyzed = True
            repo_obj.analyzed_time = timezone.now()
            repo_obj.save(
                update_fields=[
                    "analyzed",
                    "analyzed_time",
                ]
            )

        logger.info(
            f"Repository {repo_obj.git_url} fully analyzed, attempting delete"
        )

        repo_local_path = get_repo_local_path(repo_obj)
        shutil.rmtree(str(repo_local_path), ignore_errors=True)

        logger.info(
            f"Repository {repo_obj.git_url} files deleted successfully"
        )
