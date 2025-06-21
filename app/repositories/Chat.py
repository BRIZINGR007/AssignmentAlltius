from typing import List
from app.interfaces.Chat import ChatModelTH
from app.models.Chat import ChatModel
from app.repositories import BaseRepository


class ChatRepostory(BaseRepository):
    @classmethod
    def insert_one(cls, payload: ChatModelTH) -> None:
        cls._get_collection(ChatModel).insert_one(
            payload,
        )

    @classmethod
    def get_all_chats(cls, userId: str = "") -> List[ChatModelTH]:
        projection = {"_id": 0}
        return list(
            cls._get_collection(ChatModel).find(
                filter={"userId": userId},
                projection=projection,
            )
        )

    @classmethod
    def delete_all_chats(cls, userId: str = "") -> int:
        filter_query = {"userId": userId} if userId else {}
        result = cls._get_collection(ChatModel).delete_many(filter_query)
        return result.deleted_count
