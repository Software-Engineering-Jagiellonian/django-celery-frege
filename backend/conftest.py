import pytest

from frege.repositories.factories import RepositoryFactory
from frege.repositories.models import Repository


@pytest.fixture()
def dummy_repo() -> Repository:
    return RepositoryFactory(name="dummy_repo")
