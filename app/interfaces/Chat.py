from typing import Any, Dict, List, TypedDict


class ChatModelTH(TypedDict):
    chatId: str
    userId: str
    user_question: str
    reference: List[Dict[str, Any]]
    ai_answer: str
