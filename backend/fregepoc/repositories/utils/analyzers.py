from contextlib import contextmanager
from pathlib import Path

from fregepoc.repositories.models import RepositoryFile
from fregepoc.repositories.utils.paths import get_repo_local_path


@contextmanager
def repo_file_content(repo_file_obj: RepositoryFile):
    file_abs_path = (
        Path(get_repo_local_path(repo_file_obj.repository))
        / repo_file_obj.repo_relative_file_path
    )
    with open(file_abs_path, "r") as f:
        yield f.read()
