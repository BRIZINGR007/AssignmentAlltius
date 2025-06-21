from typing import cast
from app.interfaces.User import UserModelTH
from app.models.User import UserModel
from app.repositories import BaseRepository


class UserRepository(BaseRepository):
    @classmethod
    def add_user(cls, payload: UserModelTH) -> None:
        cls._get_collection(UserModel).insert_one(payload)

    @classmethod
    def get_user_by_email(cls, email: str) -> UserModelTH:
        projection = {"_id": 0}
        user = cls._get_collection(UserModel).find_one(
            {"email": email}, projection=projection
        )
        return cast(UserModelTH, user)
