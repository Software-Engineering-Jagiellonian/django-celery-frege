import pytest

from fregepoc.repositories.factories import RepositoryFactory
from fregepoc.repositories.models import Repository


@pytest.fixture()
def dummy_repo() -> Repository:
    return RepositoryFactory(name="dummy_repo")