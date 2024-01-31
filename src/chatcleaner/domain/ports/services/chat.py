import abc


class ChatServiceInterface(abc.ABC):
    def clean(self, chat_text: str) -> str:
        return self._clean(chat_text)

    @abc.abstractmethod
    def _clean(self, chat_text: str) -> str:
        raise NotImplementedError
