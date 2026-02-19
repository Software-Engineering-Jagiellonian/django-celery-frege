import pytest
from django.core.validators import URLValidator

from frege.repositories.constants import (
    CommitMessagesTypes,
    ProgrammingLanguages,
    get_extensions_for_language,
)
from frege.repositories.factories import (
    RepositoryFactory,
    RepositoryFileFactory,
    EmptyRepositoryCommitMessagesQualityFactory,
    CommitMessageFactory,
)
from frege.repositories.models import (
    Repository, 
    RepositoryFile,
    CommitMessage,
    RepositoryCommitMessagesQuality
)


@pytest.mark.django_db
class TestRepositoryModel:
    def test_create(self):
        repo_obj: Repository = RepositoryFactory()
        assert (
            not repo_obj.analyzed
        ), "The newly created repo must not be analyzed"
        url_validator = URLValidator()
        url_validator(repo_obj.repo_url)
    def test_str_method(self):
        repo_obj: Repository = RepositoryFactory()
        assert str(repo_obj) == repo_obj.name, "The __str__ method must return the name of the repo"


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
    def test_str_method(self):
        repo_file_obj: RepositoryFile = RepositoryFileFactory()
        #method
        # def __str__(self):
        # return f"file: {self.repository.name}/{self.repo_relative_file_path}"
        assert (
            str(repo_file_obj) == f"file: {repo_file_obj.repository.name}/{repo_file_obj.repo_relative_file_path}"
        ), "The __str__ method must return the name of the repo and the relative file path"

@pytest.mark.django_db
class TestRepositoryCommitMessagesQuality:
    def test_create_commit_messages_quality(self):
        empty_commit_messages_quality: RepositoryCommitMessagesQuality = EmptyRepositoryCommitMessagesQualityFactory()
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

@pytest.mark.django_db
class TestCommitMessageModel:
    def test_create_commit_message(self):
        commit_message: CommitMessage = CommitMessageFactory()
        # The newly created commit message must not be analyzed
        assert not commit_message.analyzed
        # The fields related to commit message analaze
        assert commit_message.commit_type is CommitMessagesTypes.UNCLASSIFIED
        assert commit_message.commit_message_char_length == 0
        assert commit_message.words_amount == 0
        assert commit_message.average_word_length == 0
        assert commit_message.fog_index == 0