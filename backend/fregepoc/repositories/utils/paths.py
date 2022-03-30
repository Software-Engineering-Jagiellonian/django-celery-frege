from collections.abc import Generator
from pathlib import Path

from django.conf import settings
from github import Repository as GitHubRepository

from fregepoc.repositories.constants import (
    get_languages_by_extension,
    ProgrammingLanguages,
)
from fregepoc.repositories import models


def get_repo_local_path(repo: models.Repository) -> Path:
    return Path(settings.DOWNLOAD_PATH) / repo.name


def get_repo_files(
    repo_obj: GitHubRepository,
) -> Generator[tuple[str, ProgrammingLanguages]]:
    for file_path in repo_obj.git.ls_files().split("\n"):
        extension = Path(file_path).suffix
        for lang in get_languages_by_extension(extension):
            yield file_path, lang
