import abc
from typing import Any

from chatcleaner.domain.ports.services.chat import ChatServiceInterface
from chatcleaner.domain.ports.unit_of_works.cleaning import CleaningUnitOfWorkInterface


class CleanUseCaseInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: CleaningUnitOfWorkInterface, chat: ChatServiceInterface):
        raise NotImplementedError

    def clean(self, chat_text: str) -> None:
        return self._clean(chat_text)

    def get_all(self):
        return self._get_all()

    def get_by_uuid(self, uuid_: str) -> dict[str, Any]:
        return self._get_by_uuid(uuid_)

    @abc.abstractmethod
    def _clean(self, chat_text: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_uuid(self, uuid_: str) -> dict[str, Any]:
        raise NotImplementedError
