import abc


class ChatServiceInterface(abc.ABC):
    def clean(self, chat: str) -> str:
        return self._clean(chat)

    @abc.abstractmethod
    def _clean(self, chat: str) -> str:
        raise NotImplementedError
