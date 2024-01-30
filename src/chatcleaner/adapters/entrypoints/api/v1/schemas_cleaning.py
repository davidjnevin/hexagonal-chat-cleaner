import datetime

from pydantic import BaseModel


class CleaningIn(BaseModel):
    body: str


class CleaningOut(BaseModel):
    uuid: str
    chat: str
    cleaned_chat: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AllCleaningsOut(BaseModel):
    result: list[CleaningOut]


class CleaningNotFound(BaseModel):
    result: str


class SingleCleaningOut(BaseModel):
    result: CleaningOut


class CleanedChatOut(BaseModel):
    uuid: str
    cleaned_chat: str
