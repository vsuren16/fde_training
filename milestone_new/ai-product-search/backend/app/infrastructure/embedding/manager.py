import asyncio
import logging
from dataclasses import dataclass

from app.core.config import settings
from app.infrastructure.embedding.local_provider import FakeEmbeddingProvider, LocalEmbeddingProvider
from app.infrastructure.embedding.openai_provider import OpenAIEmbeddingProvider

logger = logging.getLogger(__name__)


@dataclass
class CircuitBreaker:
    failures: int = 0
    threshold: int = 3
    open_until: float = 0.0

    def is_open(self, now: float) -> bool:
        return now < self.open_until

    def success(self) -> None:
        self.failures = 0
        self.open_until = 0.0

    def fail(self, now: float) -> None:
        self.failures += 1
        if self.failures >= self.threshold:
            self.open_until = now + 30


@dataclass
class EmbeddingResult:
    vector: list[float]
    model_version: str


class EmbeddingManager:
    def __init__(self) -> None:
        self.providers = []
        if settings.use_fake_embeddings:
            self.providers = [FakeEmbeddingProvider()]
        else:
            self.providers = []
            self.providers.append(LocalEmbeddingProvider())
            if settings.openai_api_key:
                self.providers.append(OpenAIEmbeddingProvider())
        self.breakers = [CircuitBreaker() for _ in self.providers]
        self.configured_model_chain = "|".join(provider.model_version for provider in self.providers)

    async def embed(self, text: str) -> EmbeddingResult:
        now = asyncio.get_event_loop().time()
        for provider, breaker in zip(self.providers, self.breakers):
            if breaker.is_open(now):
                continue
            try:
                vector = await provider.embed(text)
                breaker.success()
                return EmbeddingResult(vector=vector, model_version=provider.model_version)
            except Exception as exc:
                breaker.fail(asyncio.get_event_loop().time())
                logger.warning(
                    "embedding_provider_failed",
                    extra={"provider": provider.model_version, "reason": str(exc)},
                )
        raise RuntimeError("All embedding providers failed")

    async def close(self) -> None:
        for provider in self.providers:
            close = getattr(provider, "close", None)
            if close:
                await close()
