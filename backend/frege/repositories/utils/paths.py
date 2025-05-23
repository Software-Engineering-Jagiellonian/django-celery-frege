from collections.abc import Generator
from pathlib import Path
from typing import Tuple

from django.conf import settings
from github import Repository as GitHubRepository

from frege.repositories import models
from frege.repositories.constants import (
    ProgrammingLanguages,
    get_languages_by_extension,
)
from frege.repositories.models import RepositoryFile


def get_repo_local_path(repo: models.Repository) -> Path:
    """
    Returns the local filesystem path to the downloaded repository.

    The path is constructed using the repository's primary key to avoid name collisions.

    Args:
        repo (models.Repository): The repository instance.

    Returns:
        Path: Absolute path to the repository's local directory.
    """
    # We use the primary key of the repository as the directory name
    # to avoid name conflicts.
    return Path(settings.DOWNLOAD_PATH) / str(repo.pk)


def get_repo_files(
    repo_obj: GitHubRepository,
) -> Generator[Tuple[str, ProgrammingLanguages]]:
    """
    Yields file paths and corresponding programming languages from a GitHub repository.

    This function uses the repository's Git interface to list all tracked files and
    determines the programming language of each file based on its extension.

    Args:
        repo_obj (GitHubRepository): GitHub repository object.

    Yields:
        Generator[Tuple[str, ProgrammingLanguages]]: Pairs of file paths and detected languages.
    """

    for file_path in repo_obj.git.ls_files().split("\n"):
        extension = Path(file_path).suffix
        for lang in get_languages_by_extension(extension):
            yield file_path, lang


def get_file_abs_path(repo_file_obj: RepositoryFile):
    """
    Returns the absolute filesystem path of a repository file.

    Constructs the full path using the repository's local directory and the file's
    relative path within the repository.

    Args:
        repo_file_obj (RepositoryFile): The repository file model instance.

    Returns:
        Path: Absolute path to the file on the local filesystem.
    """
    return (
        Path(get_repo_local_path(repo_file_obj.repository))
        / repo_file_obj.repo_relative_file_path
    )
