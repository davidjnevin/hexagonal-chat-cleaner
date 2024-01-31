import fastapi
import pytest
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
                        result[0].chat_text
                        == "\n19:10:00 from David to Everyone:\ntest 1"
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
async def test_clean_chat_endpoint_returns_cleaning(
    get_fake_container,
    async_client: AsyncClient,
    chat_text_with_times: str,
    chat_text_without_times: str,
):
    data = {"chat_text": chat_text_with_times}
    use_case = get_fake_container.cleaning_use_case()
    with app.container.cleaning_use_case.override(use_case):
        response = await async_client.post("/clean/cleanings", json=data)
        assert response.status_code == 201
        assert response.json()["uuid"] is not None
        assert {
            "chat_text": chat_text_with_times,
            "cleaned_chat": chat_text_without_times,
        }.items() <= response.json().items()


@pytest.mark.anyio
@pytest.mark.integration
async def test_clean_chat_endpoint_returns_error_if_max_length_is_exceeded(
    get_fake_container, async_client: AsyncClient
):
    use_case = get_fake_container.cleaning_use_case()
    with app.container.cleaning_use_case.override(use_case):
        too_long_chat_text = "a" * 2001
        response = await async_client.post(
            "/clean/cleanings", json={"chat_text": too_long_chat_text}
        )
        assert response.status_code == 422
        assert "ensure this value has at most" in response.json()["detail"][0]["msg"]
        assert response.json()["detail"][0]["type"] == "value_error.any_str.max_length"


@pytest.mark.anyio
@pytest.mark.integration
async def test_clean_chat_endpoint_returns_error_if_length_is_less_that_min_length(
    get_fake_container, async_client: AsyncClient
):
    use_case = get_fake_container.cleaning_use_case()
    with app.container.cleaning_use_case.override(use_case):
        too_short_chat_text = ""
        response = await async_client.post(
            "/clean/cleanings", json={"chat_text": too_short_chat_text}
        )
        assert response.status_code == 422
        assert "ensure this value has at least" in response.json()["detail"][0]["msg"]
        assert response.json()["detail"][0]["type"] == "value_error.any_str.min_length"
