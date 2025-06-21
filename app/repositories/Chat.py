from app.interfaces.Chat import ChatModelTH
from app.models.Chat import ChatModel
from app.repositories import BaseRepository


class ChatRepostory(BaseRepository):
    @classmethod
    def insert_one(cls, payload: ChatModelTH) -> None:
        cls._get_collection(ChatModel).insert_one(
            payload,
        )
