from fastapi import APIRouter, Query

from app.controllers.Chat import ChatController
from app.enums.MiscEnums import ServicePaths

router = APIRouter(
    prefix=ServicePaths.CONTEXT_PATH.value + "/chat",
    tags=["chat"],
    responses={"404": {"description": "Not found"}},
)


@router.get("/")
async def get_context(query: str = Query()):
    return ChatController().similar_documents(query=query)


@router.post("/chat-with-ai")
async def chat_with_ai(query: str = Query()):
    return ChatController().chat_with_ai(query=query)


@router.get("/get-all-chats")
async def get_all_chats():
    return ChatController().get_all_chats()


@router.delete("/delete-all-chats")
async def delete_all_chats():
    return ChatController().delete_all_chats()
