from contextlib import contextmanager

from fregepoc.repositories.models import RepositoryFile
from pathlib import Path

from fregepoc.repositories.tasks import _get_repo_local_path


@contextmanager
def repo_file_content(repo_file_obj: RepositoryFile):
    file_abs_path = (
        Path(_get_repo_local_path(repo_file_obj.repository))
        / repo_file_obj.repo_relative_file_path
    )
    with open(file_abs_path, "r") as f:
        yield f.read()
