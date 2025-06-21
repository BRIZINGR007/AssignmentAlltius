from typing import List
from app.interfaces.Embeddings import EmbeddingModelTH
from app.models.Embedding import EmbeddingModel
from app.repositories import BaseRepository


class EmbeddingRepository(BaseRepository):
    @classmethod
    def similarity_search(
        cls, query_embedding: List[float], top_k: int
    ) -> List[EmbeddingModelTH]:
        vector_search_stage = {
            "$vectorSearch": {
                "index": "embedding_vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 75,
                "limit": top_k,
            }
        }
        project_stage = {
            "$project": {
                "_id": 0,
                "vectorId": 1,
                "references": 1,
                "text": 1,
                "token": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        }
        match_stage = {"$match": {"score": {"$gte": 0.92}}}
        aggregation_pipeline = [vector_search_stage, project_stage]
        similar_embeddings = list(
            cls._get_collection(EmbeddingModel).aggregate(aggregation_pipeline)
        )
        return similar_embeddings
