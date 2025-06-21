from typing import cast
from mongoengine import Document, StringField
from decouple import config


class UserDocument(Document):
    userId = StringField(required=True)
    email = StringField(required=True)
    name = StringField(required=True)
    meta = {
        "auto_create_index": True,
        "collection": "users",
        "strict": True,
        "db_alias": cast(str, config("DB_NAME")),
    }
