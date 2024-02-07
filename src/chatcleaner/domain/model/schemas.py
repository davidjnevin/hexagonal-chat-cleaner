import datetime

from marshmallow import EXCLUDE, Schema, fields, validate
from ulid import ULID

# This can later be moved to a config file. # TODO
MAX_CHAT_LENGTH = 6500


class ChatCreateDTO(Schema):
    chat_text = fields.Str(
        required=True, validate=validate.Length(min=1, max=MAX_CHAT_LENGTH)
    )

    class Meta:
        unknown = EXCLUDE


class CleaningCreateDTO(Schema):
    uuid = fields.String(load_default=lambda: str(ULID()))
    chat_text = fields.Str(
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
