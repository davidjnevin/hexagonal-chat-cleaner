import pytest

from chatcleaner.adapters.services.chat import ChatService
from chatcleaner.domain.model.model import cleaning_factory
from chatcleaner.domain.model.schemas import CleaningCreateDTO
from tests.fake_repository import FakeCleaningRepository


@pytest.fixture(scope="module")
def get_chat_service():
    return ChatService()


@pytest.fixture(scope="module")
def chat_text_with_times():
    return "\n19:05:59 From David to Everyone:\nso far...\n19:35:48 From David to Everyone:\nOur highest priority is to satisfy the customer\nthrough early and continuous delivery\nof valuable software.\n19:36:59 From David to Everyone:\nthe highest, the lowest\n19:55:50 From David to Everyone:\nhttps://agilemanifesto.org/principles.html"


@pytest.fixture(scope="module")
def get_fake_repository():
    return FakeCleaningRepository()


@pytest.fixture(scope="module")
def get_cleaning_model_object():
    schema_ = CleaningCreateDTO()
    result = schema_.load(
        {
            "uuid": "test",
            "chat": "\n19:10:00 from David to Everyone:\ntest",
            "cleaned_chat": "test",
            # "created_at": "2021-09-25T19:05:59",
            # "updated_at": "2021-09-25T19:05:59",
        }
    )
    return cleaning_factory(**result)
