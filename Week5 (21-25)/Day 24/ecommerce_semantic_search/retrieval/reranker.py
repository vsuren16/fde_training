from __future__ import annotations

from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
        if not candidates:
            return []

        pairs = [(query, c["text"]) for c in candidates]
        scores = self.model.predict(pairs)

        enriched = []
        for c, s in zip(candidates, scores):
            row = dict(c)
            row["rerank_score"] = float(s)
            enriched.append(row)

        ranked = sorted(enriched, key=lambda x: x["rerank_score"], reverse=True)
        return ranked[:top_k]
