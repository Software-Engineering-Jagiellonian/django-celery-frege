from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone

from .common import finalize_repo_analysis
from frege.analyzers.core import AnalyzerFactory
from frege.repositories.models import (
    RepositoryFile,
)
from frege.repositories.utils.paths import (
    get_repo_local_path,
)

logger = get_task_logger(__name__)


@shared_task
def analyze_file_task(repo_file_pk) -> None:
    """
    Celery task that analyzes a single file from a repository using language-specific analyzers.

    - Fetches the file from the database.
    - Uses appropriate analyzers to collect code metrics.
    - Saves the metrics in the database.
    - Finalizes repository analysis if needed.

    Args:
        repo_file_pk (int): Primary key of the RepositoryFile to analyze.
    """

    try:
        repo_file = RepositoryFile.objects.get(pk=repo_file_pk)
    except RepositoryFile.DoesNotExist:
        logger.error(f"repo_file for pk {repo_file_pk} does not exist")
        return

    try:
        analyzers = AnalyzerFactory.make_analyzers(repo_file.language)
        if not analyzers:
            repository = repo_file.repository
            repo_file.delete()
            finalize_repo_analysis(repository)
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
            repo_file.lines_of_code = metrics_dict.get("lines_of_code", 0)
            repo_file.token_count = metrics_dict.get("token_count", 0)
            repo_file.function_count = metrics_dict.get("function_count", 0)
            repo_file.average_function_name_length = metrics_dict.get(
                "average_function_name_length", 0
            )
            repo_file.average_lines_of_code = metrics_dict.get(
                "average_lines_of_code", 0
            )
            repo_file.average_token_count = metrics_dict.get(
                "average_token_count", 0
            )
            repo_file.average_cyclomatic_complexity = metrics_dict.get(
                "average_cyclomatic_complexity", 0
            )
            repo_file.average_parameter_count = metrics_dict.get(
                "average_parameter_count", 0
            )

            repo_file.save(
                update_fields=[
                    "metrics",
                    "analyzed",
                    "analyzed_time",
                    "lines_of_code",
                    "token_count",
                    "function_count",
                    "average_function_name_length",
                    "average_lines_of_code",
                    "average_token_count",
                    "average_cyclomatic_complexity",
                    "average_parameter_count",
                ]
            )

        logger.info(f"repo_file {repo_file.repository.git_url} analyzed")
    except Exception as error:
        repo_file.analyzed = True
        repo_file.save(update_fields=["analyzed"])
        logger.error(
            f"Can't analyze file {repo_file.repo_relative_file_path} for"
            f" the repository: {repo_file.repository.name}"
        )
        logger.error(error, exc_info=True)
    finally:
        absolute_file_path = (
            get_repo_local_path(repo_file.repository)
            / repo_file.repo_relative_file_path
        )

        finalize_repo_analysis(repo_file.repository)
