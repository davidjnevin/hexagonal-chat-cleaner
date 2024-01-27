import marshmallow
import pytest

from chatcleaner.domain.model.model import Chat, chat_factory
from chatcleaner.domain.model.schemas import ChatCreateDTO


def test_if_chat_is_created():
    schema_ = ChatCreateDTO()
    result = schema_.load({"chat": "test"})
    model = Chat(**result)
    assert model.chat == "test"
