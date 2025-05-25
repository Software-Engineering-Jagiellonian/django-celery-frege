import abc
from collections.abc import Iterator
from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

from frege.repositories.models import Repository
from frege.utils.models import SingletonModel

indexers = []


class BaseIndexer(SingletonModel):
    """
    Abstract base class for defining indexers that can iterate over a set of repositories.
    It includes mechanisms for rate-limiting and tracking whether the indexer has been throttled.
    
    Attributes:
        rate_limit_timeout (timedelta): The amount of time the indexer should wait before
                                         retrying after a rate limit is exceeded.
        rate_limit_exceeded (bool): A flag indicating whether the indexer has been rate-limited.
    
    Methods:
        __iter__(self) -> Iterator[Repository]:
            An abstract method that must be implemented in subclasses to define how the 
            indexer will iterate over repositories.
    
    Subclasses of BaseIndexer should implement the __iter__ method to define their
    specific logic for iterating through a collection of Repository objects.
    """

    rate_limit_timeout = models.DurationField(
        _("rate limit timeout"),
        default=timedelta(minutes=30),
    )

    #: A variable signifying whether the indexer has been throttled.
    rate_limit_exceeded: bool = False

    def __init_subclass__(cls, *args, **kwargs):
        """
        This method is automatically called when a subclass of BaseIndexer is defined.
        It appends the subclass to the global `indexers` list to keep track of all
        the subclasses of BaseIndexer.

        Args:
            cls: The subclass that is being created.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init_subclass__(*args, **kwargs)
        indexers.append(cls)

    @abc.abstractmethod
    def __iter__(self) -> Iterator[Repository]:
        """
        Abstract method that must be implemented by subclasses to define the iteration 
        logic for repositories.

        This method should return an iterator over Repository objects.

        Returns:
            Iterator[Repository]: An iterator that yields Repository objects.
        """
        ...

    class Meta:
        abstract = True
