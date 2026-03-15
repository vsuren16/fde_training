from langchain_openai import ChatOpenAI

from app.llm.chat_models import get_chat_model


def get_openai_client() -> ChatOpenAI:
    return get_chat_model()
