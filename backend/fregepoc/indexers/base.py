import abc

indexers = []


class BaseIndexer:
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        indexers.append(cls)

    @abc.abstractmethod
    def __iter__(self):
        ...
