
import pytest

from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.models import RepositoryFile
from fregepoc.repositories.utils.analyzers import repo_file_content
from fregepoc.repositories.utils.paths import get_repo_local_path
from fregepoc.repositories.utils.tests import MOCK_DOWNLOAD_PATH


@pytest.mark.django_db
def test_get_repo_local_path(settings, dummy_repo):
    settings.DOWNLOAD_PATH = MOCK_DOWNLOAD_PATH
    assert (repo_local_path := get_repo_local_path(dummy_repo)) == MOCK_DOWNLOAD_PATH / "dummy_repo"
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
        with open( MOCK_DOWNLOAD_PATH / "dummy_repo" / "hello_world.py") as f:
            assert content == f.read()
