import numpy as np

from app.infrastructure.vector_store.base import VectorStore


class InMemoryVectorStore(VectorStore):
    def __init__(self) -> None:
        self.matrix = np.array([], dtype=np.float32)
        self.payloads: list[dict] = []

    def build(self, embeddings: list[list[float]], payloads: list[dict]) -> None:
        if not embeddings:
            self.matrix = np.array([], dtype=np.float32)
            self.payloads = []
            return
        matrix = np.array(embeddings, dtype=np.float32)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-9
        self.matrix = matrix / norms
        self.payloads = payloads

    def add(self, embedding: list[float], payload: dict) -> None:
        vector = np.array(embedding, dtype=np.float32)
        vector = vector / (np.linalg.norm(vector) + 1e-9)
        if self.matrix.size == 0:
            self.matrix = vector.reshape(1, -1)
        else:
            self.matrix = np.vstack([self.matrix, vector])
        self.payloads.append(payload)

    def search(self, query_embedding: list[float], k: int) -> list[dict]:
        if self.matrix.size == 0:
            return []
        query = np.array(query_embedding, dtype=np.float32)
        query = query / (np.linalg.norm(query) + 1e-9)
        scores = self.matrix @ query
        top_indices = np.argsort(-scores)[:k]
        return [
            {**self.payloads[idx], "similarity_score": float(scores[idx])}
            for idx in top_indices
        ]
