from marshmallow import EXCLUDE, Schema, fields


class ChatCreateDTO(Schema):
    chat = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE
