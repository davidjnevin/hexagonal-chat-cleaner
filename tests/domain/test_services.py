import marshmallow
import pytest


def test_chat_service_clean_result(get_chat_service, chat_text_with_times):
    chat: str = chat_text_with_times
    result: str = get_chat_service.clean(chat)
    assert (
        result
        == "so far...\nOur highest priority is to satisfy the customer\nthrough early and continuous delivery\nof valuable software.\nthe highest, the lowest\nhttps://agilemanifesto.org/principles.html"
    )


def test_chat_service_clean_result_with_wrong_data_type(get_chat_service):
    text: int = 123
    with pytest.raises(marshmallow.exceptions.ValidationError):
        get_chat_service.clean(text)
