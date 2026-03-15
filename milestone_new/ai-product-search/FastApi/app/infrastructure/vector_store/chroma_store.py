from __future__ import annotations

from pathlib import Path

import chromadb
import numpy as np
from chromadb.errors import InvalidArgumentError
from chromadb.errors import NotFoundError

from app.infrastructure.vector_store.base import VectorStore


class ChromaVectorStore(VectorStore):
    def __init__(self, persist_dir: str, collection_name: str) -> None:
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def build(self, embeddings: list[list[float]], payloads: list[dict]) -> None:
        try:
            existing_ids = self.collection.get(include=[]).get("ids", [])
        except NotFoundError:
            self._recreate_collection()
            existing_ids = []
        if existing_ids:
            self.collection.delete(ids=existing_ids)
        if not embeddings:
            return
        safe_payloads = [self._sanitize_metadata(payload) for payload in payloads]
        ids = [str(payload.get("id", idx)) for idx, payload in enumerate(payloads)]
        docs = [
            payload.get("short_description")
            or payload.get("description")
            or payload.get("name")
            or payload.get("product_name")
            or ""
            for payload in payloads
        ]
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=safe_payloads,
                documents=docs,
            )
        except InvalidArgumentError as exc:
            # Happens when persisted collection was created with different vector dimension.
            if "dimension" not in str(exc).lower():
                raise
            self._recreate_collection()
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=safe_payloads,
                documents=docs,
            )

    def add(self, embedding: list[float], payload: dict) -> None:
        safe_payload = self._sanitize_metadata(payload)
        doc = (
            payload.get("short_description")
            or payload.get("description")
            or payload.get("name")
            or payload.get("product_name")
            or ""
        )
        try:
            self.collection.add(
                ids=[str(payload.get("id"))],
                embeddings=[embedding],
                metadatas=[safe_payload],
                documents=[doc],
            )
        except InvalidArgumentError as exc:
            if "dimension" not in str(exc).lower():
                raise
            self._recreate_collection()
            self.collection.add(
                ids=[str(payload.get("id"))],
                embeddings=[embedding],
                metadatas=[safe_payload],
                documents=[doc],
            )

    def search(self, query_embedding: list[float], k: int) -> list[dict]:
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["metadatas", "distances"],
        )
        rows: list[dict] = []
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        for metadata, distance in zip(metadatas, distances):
            # Chroma returns cosine distance where lower is better.
            similarity = 1.0 - float(distance)
            rows.append({**metadata, "similarity_score": float(np.clip(similarity, -1.0, 1.0))})
        return rows

    @staticmethod
    def _sanitize_metadata(metadata: dict) -> dict:
        safe: dict = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)) or value is None:
                safe[key] = value
            elif isinstance(value, list):
                safe[key] = "|".join(str(x) for x in value)
            else:
                safe[key] = str(value)
        return safe

    def _recreate_collection(self) -> None:
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
