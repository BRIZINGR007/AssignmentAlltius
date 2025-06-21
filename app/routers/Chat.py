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
