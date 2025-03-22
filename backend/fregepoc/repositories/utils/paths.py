from collections.abc import Generator
from pathlib import Path
from typing import Tuple

from django.conf import settings
from github import Repository as GitHubRepository

from fregepoc.repositories import models
from fregepoc.repositories.constants import (
    ProgrammingLanguages,
    get_languages_by_extension,
)
from fregepoc.repositories.models import RepositoryFile


def get_repo_local_path(repo: models.Repository) -> Path:
    # TODO: docstring
    # We use the primary key of the repository as the directory name
    # to avoid name conflicts.
    return Path(settings.DOWNLOAD_PATH) / str(repo.pk)


def get_repo_files(
    repo_obj: GitHubRepository,
) -> Generator[Tuple[str, ProgrammingLanguages]]:
    # TODO: docstring
    for file_path in repo_obj.git.ls_files().split("\n"):
        extension = Path(file_path).suffix
        for lang in get_languages_by_extension(extension):
            yield file_path, lang


def get_file_abs_path(repo_file_obj: RepositoryFile):
    # TODO: docstring
    return (
        Path(get_repo_local_path(repo_file_obj.repository))
        / repo_file_obj.repo_relative_file_path
    )
