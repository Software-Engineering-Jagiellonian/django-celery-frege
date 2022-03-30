from contextlib import contextmanager
from pathlib import Path

from fregepoc.repositories.models import RepositoryFile
from fregepoc.repositories.utils.paths import get_file_abs_path


@contextmanager
def repo_file_content(repo_file_obj: RepositoryFile):
    # TODO: docstring
    file_abs_path = get_file_abs_path(repo_file_obj)
    with open(file_abs_path, "r") as f:
        yield f.read()
