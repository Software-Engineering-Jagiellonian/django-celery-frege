import statistics
from contextlib import contextmanager

from lizard_ext import auto_read

from frege.repositories.models import RepositoryFile
from frege.repositories.utils.paths import get_file_abs_path


@contextmanager
def repo_file_content(repo_file_obj: RepositoryFile) -> str:
    """
    Context manager that yields the contents of a repository file.

    Retrieves the absolute file path from a RepositoryFile object and returns its content using `auto_read`.

    Args:
        repo_file_obj (RepositoryFile): The file object to read.

    Yields:
        str: The content of the file as a string.
    """

    file_abs_path = get_file_abs_path(repo_file_obj)
    yield auto_read(file_abs_path)


def average_func_name_len(function_list):
    """
    Calculates the average length of function names in a list of functions.

    Args:
        function_list (list): A list of function objects with a `name` attribute.

    Returns:
        float: The average length of function names, or 0.0 if the list is empty.
    """

    func_name_lengths = [len(func.name) for func in function_list]
    return statistics.fmean(func_name_lengths) if func_name_lengths else 0.0
