import abc

from chatcleaner.domain.ports.services.chat import ChatServiceInterface
from chatcleaner.domain.ports.unit_of_works.cleaning import CleaningUnitOfWorkInterface


class CleaningUseCaseInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: CleaningUnitOfWorkInterface, chat: ChatServiceInterface):
        raise NotImplementedError

    def add(self, chat: str) -> None:
        return self._add(chat)

    @abc.abstractmethod
    def _add(self, chat: str) -> None:
        raise NotImplementedError
