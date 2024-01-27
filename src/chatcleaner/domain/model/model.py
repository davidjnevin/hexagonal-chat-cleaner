import datetime
from dataclasses import dataclass

from chatcleaner.domain.model.schemas import ChatCreateDTO


@dataclass
class Chat:
    chat: str

    def __hash__(self):
        return hash(self.chat)

    def __eq__(self, other):
        if not isinstance(other, Chat):
            return False
        return self.chat == other.chat


@dataclass
class Cleaning:
    uuid: str
    chat: str
    cleaned_chat: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def __hash__(self):
        return hash(self.uuid)


def chat_factory(**kwargs: dict[str]) -> Chat:
    schema_ = ChatCreateDTO()
    model = Chat(**kwargs)
    schema_.dump(model)
    return model


def cleaning_factory(**kwargs: dict[str]) -> Cleaning:
    return Cleaning(**kwargs)
