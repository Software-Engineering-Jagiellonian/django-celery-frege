import abc
from collections.abc import Iterator
from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

from frege.repositories.models import Repository
from frege.utils.models import SingletonModel

indexers = []


class BaseIndexer(SingletonModel):
    rate_limit_timeout = models.DurationField(
        _("rate limit timeout"),
        default=timedelta(minutes=30),
    )

    #: A variable signifying whether the indexer has been throttled.
    rate_limit_exceeded: bool = False

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        indexers.append(cls)

    @abc.abstractmethod
    def __iter__(self) -> Iterator[Repository]:
        ...

    class Meta:
        abstract = True
