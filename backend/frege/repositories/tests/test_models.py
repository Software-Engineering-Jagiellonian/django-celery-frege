import pytest
from django.core.validators import URLValidator

from frege.repositories.constants import (
    ProgrammingLanguages,
    get_extensions_for_language,
)
from frege.repositories.factories import (
    RepositoryFactory,
    RepositoryFileFactory,
)
from frege.repositories.models import Repository, RepositoryFile


@pytest.mark.django_db
class TestRepositoryModel:
    def test_create(self):
        repo_obj: Repository = RepositoryFactory()
        assert (
            not repo_obj.analyzed
        ), "The newly created repo must not be analyzed"
        url_validator = URLValidator()
        url_validator(repo_obj.repo_url)


@pytest.mark.django_db
class TestRepositoryFileModel:
    def test_create(self):
        repo_file_obj: RepositoryFile = RepositoryFileFactory()
        assert (
            not repo_file_obj.analyzed
        ), "The newly created repo file must not be analyzed"
        assert repo_file_obj.language
        assert any(
            repo_file_obj.repo_relative_file_path.endswith(extension)
            for extension in get_extensions_for_language(
                ProgrammingLanguages(repo_file_obj.language)
            )
        )
