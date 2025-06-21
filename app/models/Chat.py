from decouple import config
from mongoengine import Document, StringField, ListField, DictField


class ChatModel(Document):
    chatId = StringField(required=True)
    userId = StringField()
    user_question = StringField(required=True)
    reference = ListField(DictField())
    ai_answer = StringField(required=True)
    meta = {
        "auto_create_index": True,
        "indexes": ["userId"],
        "collection": "chats",
        "strict": True,
        "db_alias": str(config("DB_NAME")),
    }
