from __future__ import annotations

import logging
import re
import time
from pathlib import Path

from app.core.config import settings
from app.domain.auth.schemas import UserSession
from app.domain.chat.schemas import ChatAskResponse, ChatSource
from app.infrastructure.embedding.manager import EmbeddingManager
from app.infrastructure.vector_store.base import VectorStore
from app.services.llm_service import LLMService
from app.services.order_service import OrderService

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(
        self,
        embedding_manager: EmbeddingManager,
        product_vector_store: VectorStore,
        order_service: OrderService,
        policy_vector_store: VectorStore,
        llm_service: LLMService,
    ) -> None:
        self.embedding_manager = embedding_manager
        self.product_vector_store = product_vector_store
        self.order_service = order_service
        self.policy_vector_store = policy_vector_store
        self.llm_service = llm_service
        self._guardrail_pattern = re.compile(
            r"(ignore (all )?previous instructions|system prompt|jailbreak|bypass|hack)",
            re.IGNORECASE,
        )

    async def bootstrap_policy_knowledge(self) -> None:
        policy_dir = Path(settings.policy_docs_path)
        policy_dir.mkdir(parents=True, exist_ok=True)
        docs = sorted(policy_dir.glob("*.md"))
        if not docs:
            return
        chunks: list[tuple[str, str]] = []
        for file in docs:
            text = file.read_text(encoding="utf-8")
            for idx, part in enumerate(self._split_text(text, chunk_size=600)):
                chunks.append((f"{file.stem}-{idx}", part))
        if not chunks:
            return
        embeddings = []
        payloads = []
        for chunk_id, chunk_text in chunks:
            embedding = await self.embedding_manager.embed(chunk_text)
            embeddings.append(embedding.vector)
            payloads.append(
                {
                    "id": chunk_id,
                    "source_type": "policy",
                    "source_id": chunk_id,
                    "policy_text": chunk_text,
                    "embedding_model_version": embedding.model_version,
                }
            )
        self.policy_vector_store.build(embeddings, payloads)

    async def ask(self, message: str, user: UserSession | None = None) -> ChatAskResponse:
        start = time.perf_counter()
        prompt = " ".join(message.strip().split())
        used_guardrail = False
        sources: list[ChatSource] = []
        model_version_used = "rule:no-embedding"

        if self._guardrail_pattern.search(prompt):
            used_guardrail = True
            answer = (
                "I can help with products, orders, returns, refunds, and tracking only. "
                "Please ask a business-related shopping question."
            )
            return self._response(answer, used_guardrail, sources, start)

        lowered = prompt.lower()
        if any(term in lowered for term in ["order", "tracking", "track", "delivery", "shipment", "status"]):
            if not user:
                answer = "Please login to view order tracking details."
                return self._response(answer, used_guardrail, sources, start)
            orders = await self.order_service.list_orders(user)
            if not orders:
                answer = "You do not have any orders yet."
                return self._response(answer, used_guardrail, sources, start)
            latest = orders[0]
            sources.append(
                ChatSource(
                    source_type="order",
                    source_id=latest.order_id,
                    snippet=f"Status: {latest.status}, Total: INR {latest.total}",
                )
            )
            answer = (
                f"Latest order `{latest.order_id}` is `{latest.status}` with total INR {latest.total:.2f}. "
                f"It contains {len(latest.items)} items."
            )
            return self._response(answer, used_guardrail, sources, start)

        # Retrieve contextual snippets from both product vectors and policy vectors.
        query_embedding = await self.embedding_manager.embed(prompt)
        model_version_used = query_embedding.model_version
        product_hits = self.product_vector_store.search(query_embedding.vector, settings.top_k)
        policy_hits = self.policy_vector_store.search(query_embedding.vector, 2)

        for item in product_hits[:3]:
            sources.append(
                ChatSource(
                    source_type="product",
                    source_id=str(item.get("id", "unknown")),
                    snippet=(
                        f"{item.get('product_name') or item.get('name')} | "
                        f"{item.get('short_description') or ''} | "
                        f"INR {float(item.get('price', 0)):.2f}"
                    ),
                )
            )

        policy_docs: list[str] = []
        for hit in policy_hits:
            text = str(hit.get("policy_text", ""))
            policy_docs.append(text)
            sources.append(
                ChatSource(
                    source_type="policy",
                    source_id=str(hit.get("source_id", "policy")),
                    snippet=text[:220],
                )
            )

        if "return" in lowered or "refund" in lowered or "policy" in lowered:
            answer = await self._build_policy_answer_with_llm(prompt, policy_docs)
            return self._response(answer, used_guardrail, sources, start, model_version=model_version_used)

        if product_hits and float(product_hits[0].get("similarity_score", 0)) >= 0.12:
            answer = await self._build_product_answer_with_llm(prompt, product_hits)
            return self._response(answer, used_guardrail, sources, start, model_version=model_version_used)

        answer = (
            "I do not have enough relevant information to answer that accurately right now. "
            "Please ask with more details (product type, occasion, budget, or order ID)."
        )
        return self._response(answer, used_guardrail, sources, start, model_version=model_version_used)

    def _build_policy_answer(self, policy_docs: list[str]) -> str:
        if not policy_docs:
            return "Policy knowledge base is empty right now. Please check the return and refund document setup."
        summary = policy_docs[0][:320].replace("\n", " ")
        return f"Based on company policy: {summary}"

    async def _build_policy_answer_with_llm(self, prompt: str, policy_docs: list[str]) -> str:
        if not policy_docs:
            return "I do not have enough relevant information to answer that accurately right now."
        llm_text = await self.llm_service.generate_response(
            system_prompt=(
                "You are a support assistant for return/refund policy. "
                "Answer only using provided policy context."
            ),
            user_prompt=prompt,
            context_blocks=policy_docs[:3],
            max_tokens=180,
        )
        return llm_text or self._build_policy_answer(policy_docs)

    async def _build_product_answer_with_llm(self, prompt: str, product_hits: list[dict]) -> str:
        context = [
            (
                f"{x.get('product_name') or x.get('name')} | {x.get('category')} | "
                f"INR {float(x.get('price', 0)):.2f} | {x.get('short_description') or ''}"
            )
            for x in product_hits[:5]
        ]
        llm_text = await self.llm_service.generate_response(
            system_prompt=(
                "You are an e-commerce product assistant. "
                "Use only provided context and avoid unsupported claims."
            ),
            user_prompt=prompt,
            context_blocks=context,
            max_tokens=180,
        )
        if llm_text:
            return llm_text
        top = product_hits[0]
        return (
            f"Top match is {top.get('product_name') or top.get('name')} in "
            f"{top.get('color', 'standard')} color at INR {float(top.get('price', 0)):.2f}. "
            f"{top.get('short_description') or 'This product is available now.'}"
        )

    def _response(
        self,
        answer: str,
        used_guardrail: bool,
        sources: list[ChatSource],
        start: float,
        model_version: str = "rule:no-embedding",
    ) -> ChatAskResponse:
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "chat_answer_generated",
            extra={
                "latency_ms": latency_ms,
                "model_version": model_version,
                "used_guardrail": used_guardrail,
                "sources": len(sources),
            },
        )
        return ChatAskResponse(
            answer=answer,
            model_version=model_version,
            latency_ms=latency_ms,
            used_guardrail=used_guardrail,
            sources=sources,
        )

    @staticmethod
    def _split_text(text: str, chunk_size: int = 600) -> list[str]:
        clean = " ".join(text.split())
        return [clean[i : i + chunk_size] for i in range(0, len(clean), chunk_size)]
