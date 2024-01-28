import abc

from chatcleaner.domain.ports.services.chat import ChatServiceInterface
from chatcleaner.domain.ports.unit_of_works.cleaning import CleaningUnitOfWorkInterface


class CleanUseCaseInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: CleaningUnitOfWorkInterface, chat: ChatServiceInterface):
        raise NotImplementedError

    def clean(self, chat: str) -> None:
        return self._clean(chat)

    def get_all(self):
        return self._get_all()

    @abc.abstractmethod
    def _clean(self, chat: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(self):
        raise NotImplementedError
