from typing import List, cast
import uuid

import requests
from app.context.get_context import ContextUtils
from app.interfaces.Chat import ChatModelTH
from app.ioc.ioc import SingletonMeta
from app.repositories.Chat import ChatRepostory
from app.services.Embedding import EmbeddingService
from decouple import config

from app.utils.prompts import USER_PROMPT


class ChatService(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.chatrepo = ChatRepostory()

    def call_gemeni_flash(self, reference: str, query: str) -> str:
        GEMENI_KEY: str = cast(str, config("GEMENI_API_KEY"))
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMENI_KEY}"
        prompt = USER_PROMPT.format(reference=reference, question=query)
        headers = {"Content-Type": "application/json"}

        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, headers=headers, json=payload)
        llm_response = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return llm_response

    def create_chat(
        self, query: str, ai_answer: str, refernce: List[dict]
    ) -> ChatModelTH:
        context = ContextUtils().get_headers_details()
        userId = context.userId
        chat_payload = ChatModelTH(
            chatId=str(uuid.uuid4()),
            userId=userId,
            user_question=query,
            ai_answer=ai_answer,
            reference=refernce,
        )
        return chat_payload

    def chat_with_ai(self, query: str) -> ChatModelTH:
        similar_docs = self.embedding_service.do_similarity_search(query=query)
        if not similar_docs:
            ai_answer = (
                "I Don't know. I'm sorry, but I couldn't find any relevant information to answer your question "
                "based on the available data. Please try rephrasing your query or provide more context."
            )
            chat_payload = self.create_chat(
                query=query, ai_answer=ai_answer, refernce=[]
            )
        else:
            llm_ref = "\n\n".join([each_data["text"] for each_data in similar_docs])
            ai_answer = self.call_gemeni_flash(reference=llm_ref, query=query)
            references = [each_dat["references"] for each_dat in similar_docs]
            chat_payload = self.create_chat(
                query=query, ai_answer=ai_answer, refernce=references
            )
        self.chatrepo.insert_one(chat_payload.copy())
        return chat_payload

    def get_all_chats(self) -> List[ChatModelTH]:
        context = ContextUtils.get_headers_details()
        chats = self.chatrepo.get_all_chats(userId=context.userId)
        return chats

    def delete_chats(self) -> None:
        context = ContextUtils.get_headers_details()
        self.chatrepo.delete_all_chats(userId=context.userId)
