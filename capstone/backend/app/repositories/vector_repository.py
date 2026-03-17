from typing import Protocol


class VectorRepository(Protocol):
    def upsert(self, ids: list[str], documents: list[str], metadatas: list[dict]) -> None:
        ...

    def query(self, query_text: str, top_k: int, filters: dict | None = None) -> list[dict]:
        ...
