from typing import Any

from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.llm.langsmith import configure_langsmith


def get_chat_model(temperature: float | None = None) -> ChatOpenAI:
    configure_langsmith()
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=settings.openai_temperature if temperature is None else temperature,
    )


def extract_text_content(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
        return "".join(parts).strip()
    return str(content or "").strip()
