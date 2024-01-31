import re
from contextlib import contextmanager
from typing import Generator

from chatcleaner.domain.model.model import chat_factory
from chatcleaner.domain.model.schemas import ChatCreateDTO
from chatcleaner.domain.ports.services.chat import ChatServiceInterface


@contextmanager
def chat_factory_validation(chat_text: str) -> Generator:
    data_ = {"chat_text": chat_text}
    result = ChatCreateDTO().load(data_)
    yield chat_factory(**result)


class ChatService(ChatServiceInterface):
    def _clean(self, chat_text: str) -> str:
        with chat_factory_validation(chat_text) as chat:
            # Split the text into lines
            lines = chat.chat_text.splitlines()
            # Remove the lines that begin with time info from the lines list
            non_time_lines = [
                line.replace("\t", "").replace("\r", "").replace("$", "").strip()
                for line in lines
                if not re.match(r"^\d{2}:\d{2}:\d{2}", line)
            ]
            # Join the lines into a single string
            # and remove the leading
            # and trailing whitespace characters
            return "\n".join(non_time_lines).strip()
