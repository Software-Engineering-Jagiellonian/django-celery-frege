from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone

from .common import finalize_repo_analysis
from frege.repositories.commit_messages import (
    CommitMessageAnalyzer,
)
from frege.repositories.models import (
    CommitMessage,
)

logger = get_task_logger(__name__)


@shared_task
def analyze_commit_message_quality_task(commit_message_pk):
    try:
        logger.info(
            f"Attempt of analyzing commit message {commit_message_pk} quality"
        )
        commit_message = CommitMessage.objects.get(pk=commit_message_pk)
    except CommitMessage.DoesNotExist:
        logger.error(
            f"commit message for pk {commit_message_pk} does not exist"
        )
        return

    try:
        analyzed_commit_message = CommitMessageAnalyzer(commit_message.message)

        with transaction.atomic():
            commit_message.commit_type = analyzed_commit_message.commit_type
            commit_message.commit_message_char_length = (
                analyzed_commit_message.message_length
            )
            commit_message.words_amount = analyzed_commit_message.words_amount
            commit_message.average_word_length = (
                analyzed_commit_message.average_words_length
            )
            commit_message.fog_index = analyzed_commit_message.fog_index
            commit_message.analyzed = True
            commit_message.analyzed_time = timezone.now()
            commit_message.save(
                update_fields=[
                    "analyzed",
                    "analyzed_time",
                    "commit_type",
                    "fog_index",
                    "commit_message_char_length",
                    "words_amount",
                    "average_word_length",
                ]
            )
    except Exception as error:
        with transaction.atomic():
            commit_message.analyzed = True
            commit_message.analyzed_time = timezone.now()
            commit_message.save(update_fields=["analyzed", "analyzed_time"])
        logger.error(f"Can't analyze commit message {commit_message.message}")
        logger.error(error, exc_info=True)
    finally:
        logger.info(
            f"commit_message {commit_message.commit_hash} "
            f"from repository {commit_message.repository.name} analyzed successfully!"
        )
        finalize_repo_analysis(commit_message.repository)
