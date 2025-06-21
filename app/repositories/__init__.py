from pymongo.collection import Collection
from typing import Type
from mongoengine import Document


class BaseRepository:
    @staticmethod
    def _get_collection(model_class: Type[Document]) -> Collection:
        return model_class._get_collection()
