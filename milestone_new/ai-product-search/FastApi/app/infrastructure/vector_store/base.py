from abc import ABC, abstractmethod


class VectorStore(ABC):
    @abstractmethod
    def build(self, embeddings: list[list[float]], payloads: list[dict]) -> None:
        raise NotImplementedError

    @abstractmethod
    def add(self, embedding: list[float], payload: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, query_embedding: list[float], k: int) -> list[dict]:
        raise NotImplementedError
