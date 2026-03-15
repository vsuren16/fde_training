import asyncio

from langchain_openai import OpenAIEmbeddings

from app.core.config import settings
from app.llm.langsmith import configure_langsmith
from app.security.pii import sanitize_text_for_llm

_client: OpenAIEmbeddings | None = None


def get_embeddings_client() -> OpenAIEmbeddings:
    global _client
    if _client is None:
        configure_langsmith()
        _client = OpenAIEmbeddings(
            model=settings.openai_embed_model,
            api_key=settings.openai_api_key,
        )
    return _client


def embed_text(text: str) -> list[float]:
    """
    Returns a single embedding vector for the input text.
    Defensive: empty input => empty list.
    """
    text = sanitize_text_for_llm(text).sanitized_text.strip()
    if not text:
        return []

    # clamp to avoid extreme payloads
    text = text[:12000]

    return get_embeddings_client().embed_query(text)


async def embed_text_async(text: str) -> list[float]:
    return await asyncio.to_thread(embed_text, text)
