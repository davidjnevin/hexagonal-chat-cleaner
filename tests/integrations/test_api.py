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
