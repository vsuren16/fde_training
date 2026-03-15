from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    model_version: str

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError
