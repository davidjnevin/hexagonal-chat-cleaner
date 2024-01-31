import json
from typing import Any, Union

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from chatcleaner.adapters.entrypoints.api.v1.schemas_cleaning import (
    AllCleaningsOut,
    CleanedChatOut,
    CleaningIn,
    CleaningNotFound,
    SingleCleaningOut,
)
from chatcleaner.domain.ports.use_cases.clean import CleanUseCaseInterface

router = APIRouter()


@router.get("/cleanings", response_model=AllCleaningsOut)
@inject
async def get_all_cleaning(
    use_case: CleanUseCaseInterface = Depends(Provide["cleaning_use_case"]),
) -> Response:
    data = use_case.get_all()
    return Response(
        content=json.dumps(data), media_type="application/json", status_code=200
    )


@router.get(
    "/cleanings/{uuid}", response_model=Union[SingleCleaningOut, CleaningNotFound]
)
@inject
async def get_cleaning_by_uuid(
    uuid: str,
    use_case: CleanUseCaseInterface = Depends(Provide["cleaning_use_case"]),
) -> dict[str, Any]:
    data = use_case.get_by_uuid(uuid)
    return data


@router.post("/cleanings", response_model=Union[CleanedChatOut, None])
@inject
async def clean_chat(
    chat: CleaningIn,
    use_case: CleanUseCaseInterface = Depends(Provide["cleaning_use_case"]),
):
    data = use_case.clean(chat.chat_text)
    return Response(
        content=json.dumps(data), media_type="application/json", status_code=201
    )
