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


def test_if_chat_is_created_with_factory_and_wrong_type():
    schema_ = ChatCreateDTO()
    with pytest.raises(marshmallow.exceptions.ValidationError):
        result = schema_.load({"chat": 1})
        model_ = chat_factory(**result)
        assert model_.chat == "test"


def test_if_chat_create_dto_can_be_created_with_wrong_type():
    with pytest.raises(marshmallow.exceptions.ValidationError):
        schema_ = ChatCreateDTO()
        result = schema_.load({"chat": 1})
        assert result == {"chat": 1}


def test_if_chat_dto_can_be_created_with_extra_fields():
    schema_ = ChatCreateDTO()
    result = schema_.load({"chat": "test", "extra": "test"})
    # Extra fields should be excluded.
    assert result == {"chat": "test"}


def test_if_chat_dto_can_be_created_with_wrong_field_name():
    with pytest.raises(marshmallow.exceptions.ValidationError):
        schema_ = ChatCreateDTO()
        result = schema_.load({"talk": "test"})
        # Extra fields should be excluded.
        assert result == {"chat": "test"}
