from mongoengine import Document, StringField


class ChatModel(Document):
    chatId = StringField(required=True)
    sessionId = StringField(required=True)
    userId = StringField(REQUIRED=True)
