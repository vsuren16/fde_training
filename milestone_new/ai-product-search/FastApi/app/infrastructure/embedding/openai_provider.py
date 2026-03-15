from openai import AsyncOpenAI

from app.core.config import settings
from app.infrastructure.embedding.base import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.model_version = f"openai:{settings.embedding_model}"
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.embedding_timeout_seconds,
            max_retries=settings.embedding_max_retries,
        )

    async def embed(self, text: str) -> list[float]:
        if not settings.openai_api_key:
            raise RuntimeError("OpenAI API key not configured")
        response = await self.client.embeddings.create(
            model=settings.embedding_model,
            input=text,
        )
        return response.data[0].embedding

    async def close(self) -> None:
        await self.client.close()
