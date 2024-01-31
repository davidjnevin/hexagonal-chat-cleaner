import datetime

from pydantic import BaseModel  # type: ignore
from pydantic import Field

# This can later be moved to a config file. # TODO
MAX_CHAT_LENGTH = 2000


class CleaningIn(BaseModel):
    chat_text: str = Field(max_length=MAX_CHAT_LENGTH, min_length=1)


class CleaningOut(BaseModel):
    uuid: str
    chat_text: str
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
