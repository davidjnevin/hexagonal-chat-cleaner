import fastapi
import pytest
from fastapi.exceptions import HTTPException
from httpx import AsyncClient

from chatcleaner.adapters.entrypoints.api.app import app


@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_cleaning_async_api(
    get_fake_container, async_client: AsyncClient
):
    use_case = get_fake_container.cleaning_use_case()
    with app.container.cleaning_use_case.override(use_case):
        response = await async_client.get("/clean/cleanings")
        assert response.status_code == 200
        with app.container.cleaning_uow.override(get_fake_container.cleaning_uow):
            with app.container.chat_service.override(get_fake_container.chat_service):
                use_case.clean("\n19:10:00 from David to Everyone:\ntest 1")
                use_case.clean("\n19:10:00 from David to Everyone:\ntest 2")
                use_case.clean("\n19:10:00 from David to Everyone:\ntest 3")
                uow_ = get_fake_container.cleaning_uow()
                with uow_:
                    result = uow_.cleaning.get_all()
                    assert len(result) == 3
                    assert (
                        result[0].chat == "\n19:10:00 from David to Everyone:\ntest 1"
                    )
                    assert result[0].cleaned_chat == "test 1"
        response = await async_client.get("/clean/cleanings")
        assert response.status_code == 200
        assert len(response.json()["results"]) == 3


@pytest.mark.anyio
@pytest.mark.integration
async def test_get_cleaning_by_uuid_async_api(
    get_fake_container, async_client: AsyncClient
):
    use_case = get_fake_container.cleaning_use_case()
    with app.container.cleaning_use_case.override(use_case):
        response = await async_client.get("/clean/cleanings")
        data = response.json()
        uuid = data["results"][0]
        response = await async_client.get(f"/clean/cleanings/{uuid}")
        assert response.status_code == 200
        data = response.json()
        assert data["result"]["uuid"] == uuid
        assert data["result"]["cleaned_chat"] == "test 1"


@pytest.mark.anyio
@pytest.mark.integration
async def test_get_cleaning_by_uuid_async_api_with_fake_uuid_return_Not_found(
    get_fake_container, async_client: AsyncClient
):
    use_case = get_fake_container.cleaning_use_case()
    with app.container.cleaning_use_case.override(use_case):
        response = await async_client.get("/clean/cleanings/fake")
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == "Not found"


@pytest.mark.anyio
@pytest.mark.integration
async def test_clean_chat_endpoint_returns_201(
    get_fake_container,
    async_client: AsyncClient,
    chat_text_with_times: str,
    chat_text_without_times: str,
):
    use_case = get_fake_container.cleaning_use_case()
    with app.container.cleaning_use_case.override(use_case):
        response = await async_client.post(
            "/clean/cleanings", json={"body": chat_text_with_times}
        )
        assert response.status_code == 201
        assert response.json()["uuid"] is not None
        assert response.json()["cleaned_chat"] == chat_text_without_times


@pytest.mark.anyio
@pytest.mark.integration
async def test_clean_chat_endpoint_returns_error_if_max_length_is_exceeded(
    get_fake_container, async_client: AsyncClient
):
    use_case = get_fake_container.cleaning_use_case()
    with app.container.cleaning_use_case.override(use_case):
        response = await async_client.post(
            "/clean/cleanings", json={"chat": "a" * 2001}
        )
        assert response.status_code == 422
