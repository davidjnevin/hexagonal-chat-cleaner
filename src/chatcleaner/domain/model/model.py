import datetime
from dataclasses import asdict, dataclass
from typing import Any

from chatcleaner.domain.model.schemas import ChatCreateDTO


@dataclass
class Chat:
    chat_text: str

    def __hash__(self):
        return hash(self.chat_text)

    def __eq__(self, other):
        if not isinstance(other, Chat):
            return False
        return self.chat_text == other.chat_text


@dataclass
class Cleaning:
    uuid: str
    chat_text: str
    cleaned_chat: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def __hash__(self):
        return hash(self.uuid)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def chat_factory(**kwargs: dict[str]) -> Chat:
    schema_ = ChatCreateDTO()
    model = Chat(**kwargs)
    schema_.dump(model)
    return model


def cleaning_factory(**kwargs: dict[str]) -> Cleaning:
    return Cleaning(**kwargs)
