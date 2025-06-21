from fastapi.responses import JSONResponse
from app.ioc.ioc import SingletonMeta
from app.services.Embedding import EmbeddingService


class ChatController(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.__embedding_service = EmbeddingService()

    def similar_documents(self, query: str) -> JSONResponse:
        topk_docs = self.__embedding_service.do_similarity_search(query)
        return JSONResponse(status_code=201, content=topk_docs)
