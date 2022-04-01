from contextlib import contextmanager
from typing import TypedDict

from lizard import FileInformation, analyze_file
from lizard_ext import auto_read

from fregepoc.repositories.models import RepositoryFile
from fregepoc.repositories.utils.paths import get_file_abs_path


@contextmanager
def repo_file_content(repo_file_obj: RepositoryFile) -> str:
    # TODO: docstring
    file_abs_path = get_file_abs_path(repo_file_obj)
    yield auto_read(file_abs_path)


class FileInformationDict(TypedDict):
    average_nloc: int
    average_token_count: int
    average_cyclomatic_complexity: int
    CCN: int
    ND: int


def lizard_file_information_to_dict(
    file_information: FileInformation,
) -> FileInformationDict:
    # TODO: docstring
    return {
        key: getattr(file_information, key)
        for key in FileInformationDict.__annotations__
        if hasattr(file_information, key)
    }


def generic_source_code_analysis(repo_file_obj: RepositoryFile) -> FileInformationDict:
    # TODO: docstring
    with repo_file_content(repo_file_obj) as source_code:
        return lizard_file_information_to_dict(
            analyze_file.analyze_source_code(
                str(get_file_abs_path(repo_file_obj)), source_code
            )
        )
