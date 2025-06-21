from fastapi.responses import JSONResponse
from app.ioc.ioc import SingletonMeta
from app.services.Chat import ChatService
from app.services.Embedding import EmbeddingService


class ChatController(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.__embedding_service = EmbeddingService()
        self.__chat_service = ChatService()

    def similar_documents(self, query: str) -> JSONResponse:
        topk_docs = self.__embedding_service.do_similarity_search(query)
        return JSONResponse(status_code=201, content=topk_docs)

    def chat_with_ai(self, query: str) -> JSONResponse:
        chat_payload = self.__chat_service.chat_with_ai(query)
        return JSONResponse(status_code=201, content=chat_payload)
