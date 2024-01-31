import datetime
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

MAX_CHAT_LENGTH = int(os.getenv("MAX_CHAT_LENGTH"))


class CleaningIn(BaseModel):
    chat_text: str = Field(max_length=2000, min_length=1)


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
