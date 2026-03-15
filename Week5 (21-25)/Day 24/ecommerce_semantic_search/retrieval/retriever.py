from __future__ import annotations

import re
from typing import Any

import numpy as np

from ingestion.embedder import Embedder
from retrieval.vector_store import VectorStore


class Retriever:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore,
        chunks: list[dict[str, Any]],
        top_k: int = 20,
    ):
        self.embedder = embedder
        self.vector_store = vector_store
        self.chunks = chunks
        self.top_k = top_k

    @staticmethod
    def extract_filters(query: str) -> dict[str, Any]:
        filters: dict[str, Any] = {}
        under_match = re.search(r"under\s+(\d+)", query.lower())
        if under_match:
            filters["max_price"] = int(under_match.group(1))

        category_keywords = {
            "shoe": "shoes",
            "shoes": "shoes",
            "running": "shoes",
            "watch": "wearables",
            "smartwatch": "wearables",
            "bottle": "accessories",
            "mat": "fitness",
        }
        for token in re.findall(r"[a-zA-Z]+", query.lower()):
            if token in category_keywords:
                filters["category"] = category_keywords[token]
                break
        return filters

    @staticmethod
    def apply_metadata_filter(candidates: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]:
        out = candidates
        max_price = filters.get("max_price")
        category = filters.get("category")
        if max_price is not None:
            out = [c for c in out if c.get("price") is not None and c["price"] <= max_price]
        if category:
            out = [c for c in out if str(c.get("category", "")).lower() == category.lower()]
        return out

    def retrieve(self, query: str) -> dict[str, Any]:
        q_vec = self.embedder.encode([query])
        scores, indices = self.vector_store.search(q_vec.astype(np.float32), self.top_k)

        raw_candidates: list[dict[str, Any]] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            chunk = dict(self.chunks[idx])
            chunk["vector_score"] = float(score)
            raw_candidates.append(chunk)

        filters = self.extract_filters(query)
        filtered = self.apply_metadata_filter(raw_candidates, filters)

        deduped: dict[Any, dict[str, Any]] = {}
        for item in filtered:
            pid = item.get("product_id")
            current = deduped.get(pid)
            if current is None or item["vector_score"] > current["vector_score"]:
                deduped[pid] = item

        candidates = sorted(deduped.values(), key=lambda x: x["vector_score"], reverse=True)
        return {
            "filters": filters,
            "pre_rerank": candidates,
        }
