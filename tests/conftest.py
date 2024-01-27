import pytest

from chatcleaner.adapters.services.chat import ChatService


@pytest.fixture(scope="module")
def get_chat_service():
    return ChatService()


@pytest.fixture(scope="module")
def chat_text_with_times():
    return "\n19:05:59 From David to Everyone:\nso far...\n19:35:48 From David to Everyone:\nOur highest priority is to satisfy the customer\nthrough early and continuous delivery\nof valuable software.\n19:36:59 From David to Everyone:\nthe highest, the lowest\n19:55:50 From David to Everyone:\nhttps://agilemanifesto.org/principles.html"
