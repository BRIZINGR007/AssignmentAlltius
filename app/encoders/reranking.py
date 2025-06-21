from typing import List
from app.interfaces.Embeddings import EmbeddingModelTH
from app.ioc.ioc import SingletonMeta
from flashrank import Ranker, RerankRequest


class Reranking(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.rankerMiniLm = Ranker(
            model_name="ms-marco-MiniLM-L-12-v2",
            cache_dir="ONNX-ms-marco-MiniLM-L-12-v2",
        )

    def rerank_top_k_docs(
        self,
        query: str,
        passages: List[EmbeddingModelTH],
    ):
        rerankrequest = RerankRequest(query=query, passages=passages)
        reranked_docs = self.rankerMiniLm.rerank(rerankrequest)[:2]
        filtered_docs: List[EmbeddingModelTH] = [
            item for item in reranked_docs if item["score"] > 0.01
        ]
        return filtered_docs
