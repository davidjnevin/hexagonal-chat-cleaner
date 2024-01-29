from fastapi import APIRouter

from chatcleaner.adapters.entrypoints.api.v1 import route_cleaning

api_router = APIRouter()

api_router.include_router(
    route_cleaning.router,
    # prefix="/clean",
    tags=["clean"],
)
