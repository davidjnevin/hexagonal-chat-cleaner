import marshmallow
import pytest

from chatcleaner.domain.model.model import Chat, chat_factory
from chatcleaner.domain.model.schemas import ChatCreateDTO


def test_if_chat_is_created():
    schema_ = ChatCreateDTO()
    result = schema_.load({"chat": "test"})
    model_ = Chat(**result)
    assert model_.chat == "test"


def test_if_chat_is_created_with_factory():
    schema_ = ChatCreateDTO()
    result = schema_.load({"chat": "test"})
    model_ = chat_factory(**result)
    assert model_.chat == "test"
