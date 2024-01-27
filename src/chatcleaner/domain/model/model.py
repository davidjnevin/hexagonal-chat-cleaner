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


def chat_factory(**kwargs: dict[str]) -> Chat:
    schema_ = ChatCreateDTO()
    model = Chat(**kwargs)
    schema_.dump(model)
    return model
