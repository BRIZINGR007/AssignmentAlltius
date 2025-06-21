import logging
from decouple import config
from pymongo.errors import OperationFailure
from mongoengine import (
    Document,
    ListField,
    StringField,
    DictField,
    get_db,
    FloatField,
    IntField,
)

logger = logging.getLogger(__name__)


class EmbeddingModel(Document):
    vectorId = StringField(required=True)
    references = DictField(required=True)
    text = StringField(required=True)
    token = IntField(required=True)
    embedding = ListField(FloatField(), required=True)

    meta = {
        "auto_create_index": True,
        "indexes": [],
        "collection": "embeddings",
        "strict": True,
        "db_alias": str(config("DB_NAME")),
    }

    @classmethod
    def ensure_indexes(cls):
        super().ensure_indexes()
        cls.ensure_vector_search_index()

    @staticmethod
    def ensure_vector_search_index():
        try:
            db = get_db(alias=str(config("DB_NAME")))
            collection = db["embeddings"]
            index_model = {
                "name": "embedding_vector_index",
                "definition": {
                    "fields": [
                        {
                            "type": "vector",
                            "path": "embedding",
                            "numDimensions": 64,
                            "similarity": "dotProduct",
                        },
                    ]
                },
                "type": "vectorSearch",
            }

            collection.create_search_index(model=index_model)
        except OperationFailure as e:
            if "already exists" in str(e):
                logger.info(msg="Vector search index already exists.")
            else:
                logger.error(f"Failed to create vector search index: {e}")
        except Exception as e:
            logger.error(f" Unexpected error creating vector index: {e}")
