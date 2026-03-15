from __future__ import annotations

import logging
from datetime import datetime, timezone

from config import ENABLE_JUDGE_DEFAULT
from evaluation.judge import Judge
from evaluation.metrics_store import MetricsStore
from generation.llm_generator import LLMGenerator
from retrieval.reranker import Reranker
from retrieval.retriever import Retriever

logger = logging.getLogger(__name__)


class EcommercePipeline:
    def __init__(
        self,
        retriever: Retriever,
        reranker: Reranker,
        generator: LLMGenerator,
        judge: Judge,
        metrics_store: MetricsStore,
        enable_judge: bool = ENABLE_JUDGE_DEFAULT,
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.generator = generator
        self.judge = judge
        self.metrics_store = metrics_store
        self.enable_judge = enable_judge

    def set_reranker(self, reranker: Reranker) -> None:
        self.reranker = reranker

    def set_judge_enabled(self, enabled: bool) -> None:
        self.enable_judge = enabled

    async def run(self, query: str) -> dict:
        retrieved = self.retriever.retrieve(query)
        pre_rerank = retrieved["pre_rerank"]
        ranked = self.reranker.rerank(query, pre_rerank)
        llm_explanation = await self.generator.generate(query, ranked)

        evaluation_score = {
            "relevance": 0,
            "faithfulness": 0,
            "completeness": 0,
            "overall_score": 0.0,
            "reasoning": "Judge disabled",
        }
        if self.enable_judge:
            evaluation_score = await self.judge.evaluate(query, ranked, llm_explanation)

        payload = {
            "query": query,
            "filters": retrieved.get("filters", {}),
            "products": ranked,
            "pre_rerank_order": [p.get("product_id") for p in pre_rerank],
            "post_rerank_order": [p.get("product_id") for p in ranked],
            "llm_explanation": llm_explanation,
            "evaluation_score": evaluation_score,
        }

        self.metrics_store.append(
            {
                "query": query,
                "retrieved_products": payload["pre_rerank_order"],
                "reranked_products": payload["post_rerank_order"],
                "llm_explanation": llm_explanation,
                "evaluation_score": evaluation_score,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "model_versions": {
                    "embedder": getattr(self.retriever.embedder, "model_name", "unknown"),
                    "reranker": getattr(self.reranker, "model_name", "unknown"),
                    "generator": getattr(self.generator, "model", "unknown"),
                    "judge": getattr(self.judge, "model", "unknown"),
                },
            }
        )
        logger.info("Search handled", extra={"query": query, "products": payload["post_rerank_order"]})
        return payload

    async def run_batch(self, queries: list[str]) -> list[dict]:
        out = []
        for q in queries:
            out.append(await self.run(q))
        return out
