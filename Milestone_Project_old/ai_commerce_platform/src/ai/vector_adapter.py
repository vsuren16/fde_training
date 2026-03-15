"""Vector retrieval adapter contract for future decoupling."""

from __future__ import annotations

from typing import Protocol


class VectorStoreAdapter(Protocol):
    def index(self, item_id: str, vector: list[float]) -> None:
        ...

    def query(self, vector: list[float], top_k: int) -> list[tuple[str, float]]:
        ...
