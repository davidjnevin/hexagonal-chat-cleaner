import datetime

from marshmallow import EXCLUDE, Schema, fields, validate
from ulid import ULID

# This can later be moved to a config file.
MAX_CHAT_LENGTH = 2000


class ChatCreateDTO(Schema):
    chat = fields.Str(
        required=True, validate=validate.Length(min=1, max=MAX_CHAT_LENGTH)
    )

    class Meta:
        unknown = EXCLUDE


class CleaningCreateDTO(Schema):
    uuid = fields.String(load_default=lambda: str(ULID()))
    chat = fields.Str(
        required=True, validate=validate.Length(min=1, max=MAX_CHAT_LENGTH)
    )
    cleaned_chat = fields.Str(
        required=True, validate=validate.Length(min=1, max=MAX_CHAT_LENGTH)
    )
    created_at = fields.DateTime(
        load_default=datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at = fields.DateTime(
        load_default=datetime.datetime.now(datetime.timezone.utc)
    )

    class Meta:
        unknown = EXCLUDE
