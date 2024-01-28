import json

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from chatcleaner.domain.ports.use_cases.clean import CleanUseCaseInterface

router = APIRouter()


@router.post("/clean", response_model=None)
@inject
async def get_all_cleaning(
    use_case: CleanUseCaseInterface = Depends(Provide["clean_use_case"]),
) -> Response:
    data = use_case.get_all()
    return Response(
        content=json.dumps(data), media_type="application/json", status_code=200
    )
