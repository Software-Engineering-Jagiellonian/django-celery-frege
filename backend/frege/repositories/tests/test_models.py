import pytest
from django.core.validators import URLValidator

from frege.repositories.constants import (
    ProgrammingLanguages,
    get_extensions_for_language,
)
from frege.repositories.factories import (
    RepositoryFactory,
    RepositoryFileFactory,
    EmptyRepositoryCommitMessagesQualityFactory
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

@pytest.mark.django_db
class TestRepositoryCommitMessagesQuality:
    def test_create_commit_messages_quality(self):
        empty_commit_messages_quality = EmptyRepositoryCommitMessagesQualityFactory()
        # The newly created commit messages quality must not be analyzed
        assert not empty_commit_messages_quality.analyzed
        # The fields realted to commit messages quality must be 0 at the beginning
        assert empty_commit_messages_quality.commits_amount == 0
        assert empty_commit_messages_quality.average_commit_message_characters_length == 0
        assert empty_commit_messages_quality.average_commit_message_words_amount == 0
        assert empty_commit_messages_quality.average_commit_message_fog_index == 0
        assert empty_commit_messages_quality.classifiable_to_unclassifiable_commit_messages_ratio == 0
        assert empty_commit_messages_quality.percentage_of_feature_commits == 0
        assert empty_commit_messages_quality.percentage_of_fix_commits == 0
        assert empty_commit_messages_quality.percentage_of_config_change_commits == 0
        assert empty_commit_messages_quality.percentage_of_merge_pr_commits == 0
        assert empty_commit_messages_quality.percentage_of_unclassified_commits == 0

