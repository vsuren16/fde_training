from __future__ import annotations

from collections.abc import Sequence

import chromadb

from app.core.config import get_settings


class ChromaVectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection,
            metadata={"hnsw:space": "cosine"},
        )

    def upsert(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def query(
        self,
        query_embedding: list[float],
        top_k: int,
        where: dict | None = None,
    ) -> list[dict]:
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )
        ids: Sequence[str] = result.get("ids", [[]])[0]
        distances: Sequence[float] = result.get("distances", [[]])[0]
        metadatas: Sequence[dict] = result.get("metadatas", [[]])[0]
        documents: Sequence[str] = result.get("documents", [[]])[0]

        items: list[dict] = []
        for incident_id, distance, metadata, document in zip(
            ids, distances, metadatas, documents
        ):
            items.append(
                {
                    "incident_id": incident_id,
                    "distance": float(distance),
                    "metadata": metadata or {},
                    "document": document,
                }
            )
        return items

    def count(self) -> int:
        return self.collection.count()

    def reset(self) -> None:
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"},
        )


class NoOpVectorStore:
    def upsert(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        return None

    def query(
        self,
        query_embedding: list[float],
        top_k: int,
        where: dict | None = None,
    ) -> list[dict]:
        return []

    def count(self) -> int:
        return 0

    def reset(self) -> None:
        return None
