import marshmallow
import pytest

from chatcleaner.domain.model.model import (
    Chat,
    Cleaning,
    chat_factory,
    cleaning_factory,
)
from chatcleaner.domain.model.schemas import ChatCreateDTO, CleaningCreateDTO


def test_if_chat_is_created():
    schema_ = ChatCreateDTO()
    result = schema_.load({"chat_text": "test"})
    model_ = Chat(**result)
    assert model_.chat_text == "test"


def test_if_chat_is_created_with_factory():
    schema_ = ChatCreateDTO()
    result = schema_.load({"chat_text": "test"})
    model_ = chat_factory(**result)
    assert model_.chat_text == "test"


def test_if_chat_is_created_with_factory_and_wrong_type():
    schema_ = ChatCreateDTO()
    with pytest.raises(marshmallow.exceptions.ValidationError):
        result = schema_.load({"chat_text": 1})
        model_ = chat_factory(**result)
        assert model_.chat_text == "test"


def test_if_chat_create_dto_can_be_created_with_wrong_type():
    with pytest.raises(marshmallow.exceptions.ValidationError):
        schema_ = ChatCreateDTO()
        result = schema_.load({"chat_text": 1})
        assert result == {"chat_text": 1}


def test_if_chat_dto_can_be_created_with_extra_fields():
    schema_ = ChatCreateDTO()
    result = schema_.load({"chat_text": "test", "extra": "test"})
    # Extra fields should be excluded.
    assert result == {"chat_text": "test"}


def test_if_chat_dto_can_be_created_with_wrong_field_name():
    with pytest.raises(marshmallow.exceptions.ValidationError):
        schema_ = ChatCreateDTO()
        result = schema_.load({"talk": "test"})
        assert result == {"chat_text": "test"}


def test_if_chat_dto_can_be_created_with_empty_string():
    with pytest.raises(marshmallow.exceptions.ValidationError):
        schema_ = ChatCreateDTO()
        result = schema_.load({"chat_text": ""})
        assert result == {"chat_text": ""}


def test_if_chat_dto_can_be_created_with_more_than_2000_characters():
    with pytest.raises(marshmallow.exceptions.ValidationError):
        schema_ = ChatCreateDTO()
        dirty_text = "a" * 2001
        result = schema_.load({"chat_text": dirty_text})
        assert result == {"chat_text": dirty_text}


def test_if_cleaning_is_created():
    schema_ = CleaningCreateDTO()
    result = schema_.load(
        {"chat_text": "\n19:00:54 David said:\ntest", "cleaned_chat": "test"}
    )
    model_ = Cleaning(**result)
    assert model_.chat_text == "\n19:00:54 David said:\ntest"
    assert model_.cleaned_chat == "test"
    assert model_.created_at is not None
    assert model_.updated_at is not None


def test_if_cleaning_is_created_with_factory():
    schema_ = CleaningCreateDTO()
    result = schema_.load(
        {"chat_text": "\n19:00:54 David said:\ntest", "cleaned_chat": "test"}
    )
    model_ = cleaning_factory(**result)
    assert model_.chat_text == "\n19:00:54 David said:\ntest"
    assert model_.cleaned_chat == "test"


def test_if_cleaning_is_created_with_factory_and_wrong_type():
    schema_ = CleaningCreateDTO()
    with pytest.raises(marshmallow.exceptions.ValidationError):
        result = schema_.load({"chat_text": 1, "cleaned_chat": "test"})
        model_ = cleaning_factory(**result)
        assert model_.chat_text == "\n19:00:54 David said:\ntest"
        assert model_.cleaned_chat == "test"
    with pytest.raises(marshmallow.exceptions.ValidationError):
        result = schema_.load({"chat_text": "text", "cleaned_chat": 1})
        model_ = cleaning_factory(**result)
        assert model_.chat_text == "\n19:00:54 David said:\ntest"
        assert model_.cleaned_chat == "test"


def test_if_cleaning_is_created_with_empty_strings():
    schema_ = CleaningCreateDTO()
    with pytest.raises(marshmallow.exceptions.ValidationError):
        result = schema_.load({"chat_text": "", "cleaned_chat": "test"})
        model_ = cleaning_factory(**result)
        assert model_.chat_text == ""
        assert model_.cleaned_chat == "test"
    with pytest.raises(marshmallow.exceptions.ValidationError):
        result = schema_.load(
            {"chat_text": "\n19:00:54 David said:\ntest", "cleaned_chat": ""}
        )
        model_ = cleaning_factory(**result)
        assert model_.chat_text == "\n19:00:54 David said:\ntest"
        assert model_.cleaned_chat == "test"


def test_if_cleaning_is_created_with_more_than_2000_characters():
    schema_ = CleaningCreateDTO()
    with pytest.raises(marshmallow.exceptions.ValidationError):
        dirty_text = "a" * 2001
        result = schema_.load({"chat_text": dirty_text, "cleaned_chat": "test"})
        model_ = cleaning_factory(**result)
        assert model_.chat_text == dirty_text
        assert model_.cleaned_chat == "test"
    with pytest.raises(marshmallow.exceptions.ValidationError):
        dirty_text = "a" * 2001
        result = schema_.load(
            {"chat_text": "\n19:00:54 David said:\ntest", "cleaned_chat": dirty_text}
        )
        model_ = cleaning_factory(**result)
        assert model_.chat_text == "\n19:00:54 David said:\ntest"
        assert model_.cleaned_chat == dirty_text
