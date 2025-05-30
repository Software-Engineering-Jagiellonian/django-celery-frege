import random
from operator import itemgetter

import factory.fuzzy
from faker import Faker

from frege.repositories.constants import (
    ProgrammingLanguages,
    get_extensions_for_language,
)

from frege.repositories.models import (
    Repository, 
    RepositoryFile, 
    RepositoryCommitMessagesQuality,
    CommitMessage
)

faker_obj = Faker()


class RepositoryFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating instances of the Repository model for generating test data.
    
    Attributes:
        name (str): The repository name (unique for each instance).
        git_url (str): A GitHub URL for the repository, generated based on the repository name.
        repo_url (str): A randomly generated URL for the repository.
        commit_hash (str): A random SHA-1 hash simulating a commit hash.
    """ 
    class Meta:
        model = Repository

    name = factory.Sequence(lambda n: f"repo_{n}")
    git_url = factory.LazyAttribute(
        lambda obj: f"git@github.com:{faker_obj.user_name}/{obj.name}.git"
    )
    repo_url = factory.Faker("url")
    commit_hash = factory.Faker("sha1", raw_output=False)


class RepositoryFileFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating instances of the RepositoryFile model for generating test data.
    
    Attributes:
        repository (Repository): The repository associated with the file.
        language (str): A randomly selected programming language assigned to the file.
        repo_relative_file_path (str): The file path within the repository, generated based on the selected language and file extension.
    """
    class Meta:
        model = RepositoryFile

    repository = factory.SubFactory(RepositoryFactory)
    language = factory.fuzzy.FuzzyChoice(
        choices=ProgrammingLanguages.choices, getter=itemgetter(0)
    )
    repo_relative_file_path = factory.LazyAttribute(
        lambda obj: faker_obj.file_path(
            extension=random.choice(
                get_extensions_for_language(ProgrammingLanguages(obj.language))
            )
        )
    )

class EmptyRepositoryCommitMessagesQualityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RepositoryCommitMessagesQuality

    repository = factory.SubFactory(RepositoryFactory)

class CommitMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommitMessage

    repository = factory.SubFactory(RepositoryFactory)
    author = faker_obj.user_name()
    commit_hash = factory.Faker("sha1", raw_output=False)
    message = factory.Faker("text", max_nb_chars=200)