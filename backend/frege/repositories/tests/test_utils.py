import pytest
from pytest_mock import MockerFixture
from pytest_unordered import unordered

from frege.repositories.constants import ProgrammingLanguages
from frege.repositories.models import RepositoryFile
from frege.repositories.utils.analyzers import repo_file_content
from frege.repositories.utils.paths import (
    get_repo_files,
    get_repo_local_path,
)
from frege.repositories.utils.tests import MOCK_DOWNLOAD_PATH


@pytest.mark.django_db
def test_get_repo_local_path(settings, dummy_repo):
    settings.DOWNLOAD_PATH = MOCK_DOWNLOAD_PATH
    assert (
        repo_local_path := get_repo_local_path(dummy_repo)
    ) == MOCK_DOWNLOAD_PATH / "dummy_repo"
    assert repo_local_path.exists()


@pytest.mark.django_db
def test_repo_file_content(settings, dummy_repo):
    settings.DOWNLOAD_PATH = MOCK_DOWNLOAD_PATH
    repo_file = RepositoryFile(
        repository=dummy_repo,
        repo_relative_file_path="hello_world.py",
        language=ProgrammingLanguages.PYTHON,
    )
    with repo_file_content(repo_file) as content:
        with open(MOCK_DOWNLOAD_PATH / "dummy_repo" / "hello_world.py") as f:
            assert content == f.read()


def test_get_repo_files(mocker: MockerFixture):
    repo_obj_mock = mocker.MagicMock()
    repo_obj_mock.git.ls_files = lambda: "ans.cpp\nhello_world.py"
    assert list(get_repo_files(repo_obj_mock)) == unordered(
        [
            ("ans.cpp", ProgrammingLanguages.CPP),
            ("hello_world.py", ProgrammingLanguages.PYTHON),
        ]
    )
