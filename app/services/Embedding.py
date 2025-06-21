from typing import Any
from app.encoders.embedidng_generator import EmbeddingGenerator
from app.ioc.ioc import SingletonMeta
from app.repositories.Embedding import EmbeddingRepository


class EmbeddingService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.embedding_generator = EmbeddingGenerator()
        self.embedding_repo = EmbeddingRepository()

    def do_similarity_search(self, query: str) -> Any:
        embedding = self.embedding_generator.get_embeddings(query)
        similar_vectors = self.embedding_repo.similarity_search(
            query_embedding=embedding, top_k=5
        )
        return similar_vectors
