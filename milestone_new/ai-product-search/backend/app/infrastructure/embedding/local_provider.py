import asyncio
import hashlib
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.infrastructure.embedding.base import EmbeddingProvider


class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.model_version = f"local:{settings.local_embedding_model}"
        self.model = None

    def _ensure_model(self) -> SentenceTransformer:
        if self.model is None:
            self.model = SentenceTransformer(settings.local_embedding_model)
        return self.model

    async def embed(self, text: str) -> list[float]:
        model = await asyncio.to_thread(self._ensure_model)
        vector = await asyncio.to_thread(model.encode, text, normalize_embeddings=True)
        return vector.tolist()


class FakeEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.model_version = "fake:test-embedding-v1"

    async def embed(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        vector = np.frombuffer(digest, dtype=np.uint8).astype(np.float32)
        vector = vector / (np.linalg.norm(vector) + 1e-9)
        return vector.tolist()
