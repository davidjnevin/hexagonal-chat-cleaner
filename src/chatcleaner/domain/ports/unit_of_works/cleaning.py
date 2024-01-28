import abc

from chatcleaner.domain.ports.repositories.cleaning import CleaningRespositoryInterface


class CleaningUnitOfWorkInterface(abc.ABC):
    cleaning: CleaningRespositoryInterface

    def __enter__(self) -> "CleaningUnitOfWorkInterface":
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
