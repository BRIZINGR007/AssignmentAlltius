from typing import Any, List
from app.encoders.embedidng_generator import EmbeddingGenerator
from app.encoders.reranking import Reranking
from app.interfaces.Embeddings import EmbeddingModelTH
from app.ioc.ioc import SingletonMeta
from app.repositories.Embedding import EmbeddingRepository


class EmbeddingService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.embedding_generator = EmbeddingGenerator()
        self.reranking = Reranking()
        self.embedding_repo = EmbeddingRepository()

    def do_similarity_search(self, query: str) -> List[EmbeddingModelTH]:
        embedding = self.embedding_generator.get_embeddings(query)
        similar_vectors = self.embedding_repo.similarity_search(
            query_embedding=embedding, top_k=5
        )
        reranked_docs = self.reranking.rerank_top_k_docs(
            query=query, passages=similar_vectors
        )
        return reranked_docs
