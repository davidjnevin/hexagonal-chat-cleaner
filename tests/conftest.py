import contextlib
from typing import AsyncIterator

import httpx
import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from chatcleaner.adapters.db.orm import start_mappers
from chatcleaner.adapters.entrypoints.api.app import app
from chatcleaner.adapters.services.chat import ChatService
from chatcleaner.adapters.use_cases.clean import CleanUseCase
from chatcleaner.domain.model.model import cleaning_factory
from chatcleaner.domain.model.schemas import CleaningCreateDTO
from tests.fake_container import FakeContainer
from tests.fake_repository import FakeCleaningRepository
from tests.fake_uow import FakeCleaningUnitOfWork


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def get_chat_service():
    return ChatService()


@pytest.fixture()
def chat_text_with_times() -> str:
    return "\n19:05:59 From David to Everyone:\nso far...\n19:35:48 From David to Everyone:\nOur highest priority is to satisfy the customer\nthrough early and continuous delivery\nof valuable software.\n19:36:59 From David to Everyone:\nthe highest, the lowest\n19:55:50 From David to Everyone:\nhttps://agilemanifesto.org/principles.html"


@pytest.fixture()
def chat_text_without_times() -> str:
    return "so far...\nOur highest priority is to satisfy the customer\nthrough early and continuous delivery\nof valuable software.\nthe highest, the lowest\nhttps://agilemanifesto.org/principles.html"


@pytest.fixture(scope="module")
def get_fake_repository():
    return FakeCleaningRepository()


@pytest.fixture(scope="module")
def get_cleaning_model_object():
    schema_ = CleaningCreateDTO()
    result = schema_.load(
        {
            "uuid": "test",
            "chat_text": "\n19:10:00 from David to Everyone:\ntest",
            "cleaned_chat": "test",
        }
    )
    return cleaning_factory(**result)


@pytest.fixture(scope="module")
def get_fake_uow():
    return FakeCleaningUnitOfWork()


@pytest.fixture(scope="module")
def get_fake_container():
    # Start orm mapper
    with contextlib.suppress(sqlalchemy.exc.ArgumentError):
        start_mappers()

    # Truncate table
    uow = FakeContainer.cleaning_uow()
    with uow:
        uow.session.execute(sqlalchemy.text("DELETE FROM cleaning"))
        uow.commit()

    return FakeContainer()


@pytest.fixture(scope="module")
def get_clean_use_case():
    return CleanUseCase()


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client_:
        yield client_


@pytest.fixture()
async def async_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url="http://test") as client_:
        yield client_
