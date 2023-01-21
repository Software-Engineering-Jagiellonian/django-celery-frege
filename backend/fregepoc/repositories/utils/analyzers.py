import statistics
from contextlib import contextmanager

from lizard_ext import auto_read

from fregepoc.repositories.models import RepositoryFile
from fregepoc.repositories.utils.paths import get_file_abs_path


@contextmanager
def repo_file_content(repo_file_obj: RepositoryFile) -> str:
    # TODO: docstring
    file_abs_path = get_file_abs_path(repo_file_obj)
    yield auto_read(file_abs_path)


def average_func_name_len(function_list):
    # TODO: docstring
    func_name_lengths = [len(func.name) for func in function_list]
    return statistics.fmean(func_name_lengths) if func_name_lengths else 0.0
