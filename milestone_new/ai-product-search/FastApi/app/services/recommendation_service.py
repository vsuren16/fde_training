import logging
import time

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.langsmith import trace_run
from app.domain.recommendations.schemas import RecommendationItem, RecommendRequest, RecommendResponse
from app.infrastructure.db.repositories import SearchHistoryRepository
from app.infrastructure.embedding.manager import EmbeddingManager
from app.infrastructure.vector_store.base import VectorStore
from app.services.keyword_search_service import KeywordSearchService
from app.services.llm_service import LLMService
from app.services.product_service import ProductService

logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(
        self,
        embedding_manager: EmbeddingManager,
        vector_store: VectorStore,
        product_service: ProductService,
        keyword_search_service: KeywordSearchService,
        llm_service: LLMService,
    ) -> None:
        self.embedding_manager = embedding_manager
        self.vector_store = vector_store
        self.product_service = product_service
        self.keyword_search_service = keyword_search_service
        self.llm_service = llm_service

    async def recommend(self, req: RecommendRequest, db: AsyncSession) -> RecommendResponse:
        start = time.perf_counter()
        query = " ".join(req.prompt.lower().split())
        used_fallback = False
        model_version_used = "keyword:fallback-no-embedding"

        async with trace_run(
            "products.recommend",
            run_type="chain",
            inputs={"prompt": req.prompt, "category": req.category, "max_price": req.max_price},
            tags=["recommendation", "semantic-search"],
            metadata={"configured_model_chain": self.embedding_manager.configured_model_chain},
        ) as run:
            try:
                embedding = await self.embedding_manager.embed(query)
                model_version_used = embedding.model_version
                candidates = self.vector_store.search(embedding.vector, settings.top_k * 5)
                if not candidates:
                    raise ValueError("empty vector store")
            except Exception as exc:
                logger.warning("vector_search_failed_using_keyword_fallback", extra={"reason": str(exc)})
                used_fallback = True
                products = [p.model_dump() for p in await self.product_service.list_all_products()]
                candidates = self.keyword_search_service.rank(query, products, settings.top_k * 5)

            filtered = []
            for item in candidates:
                if not item.get("available", item.get("availability", True)):
                    continue
                if req.category and item.get("category", "").lower() != req.category.lower():
                    continue
                if req.max_price and float(item.get("price", 0)) > req.max_price:
                    continue
                filtered.append(item)

            if not filtered and not used_fallback:
                logger.warning("filtered_empty_retrying_keyword_search")
                used_fallback = True
                products = [p.model_dump() for p in await self.product_service.list_all_products()]
                filtered = self.keyword_search_service.rank(query, products, settings.top_k * 3)

            if not filtered:
                filtered = candidates[: settings.top_k * 2]

            top_items = filtered[: settings.top_k]
            normalized_items = []
            for item in top_items:
                image_urls = item.get("image_urls", [])
                if isinstance(image_urls, str):
                    image_urls = [x for x in image_urls.split("|") if x]
                normalized_items.append(
                    {
                        "id": str(item.get("id", "")),
                        "name": item.get("name") or item.get("product_name") or "Product",
                        "product_name": item.get("product_name") or item.get("name") or "Product",
                        "category": item.get("category", "General"),
                        "price": float(item.get("price", 0)),
                        "image_url": item.get("image_url", ""),
                        "image_urls": image_urls,
                        "short_description": item.get("short_description") or "",
                        "description": item.get("description") or "",
                        "brand": item.get("brand") or "",
                        "color": item.get("color") or "",
                        "size": item.get("size") or "",
                        "available": bool(item.get("available", item.get("availability", True))),
                        "similarity_score": float(item.get("similarity_score", 0)),
                    }
                )

            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            scores = [round(float(x["similarity_score"]), 4) for x in normalized_items]

            logger.info(
                "recommendation_completed",
                extra={
                    "query": query,
                    "latency_ms": latency_ms,
                    "num_results": len(normalized_items),
                    "model_version": model_version_used,
                    "configured_model_chain": self.embedding_manager.configured_model_chain,
                    "scores": scores,
                    "fallback": used_fallback,
                },
            )

            assistant_response = await self._build_recommendation_message(query, normalized_items)

            try:
                history_repo = SearchHistoryRepository(db)
                await history_repo.add_record(
                    query_text=query,
                    model_version=model_version_used,
                    latency_ms=latency_ms,
                    scores=scores,
                )
            except Exception as exc:
                logger.warning("search_history_write_failed", extra={"reason": str(exc)})

            response = RecommendResponse(
                query=query,
                model_version=model_version_used,
                latency_ms=latency_ms,
                assistant_response=assistant_response,
                results=[RecommendationItem(**item) for item in normalized_items],
            )
            run.metadata["model_version_used"] = model_version_used
            run.metadata["used_keyword_fallback"] = used_fallback
            run.end(
                outputs={
                    "query": response.query,
                    "model_version": response.model_version,
                    "latency_ms": response.latency_ms,
                    "result_count": len(response.results),
                }
            )
            return response

    async def _build_recommendation_message(self, query: str, items: list[dict]) -> str:
        if not items:
            return (
                "I could not find matching products for this query. "
                "Please try describing an occasion, style, colour, or budget."
            )

        context = [
            f"{x.get('product_name')} | {x.get('category')} | INR {x.get('price')} | {x.get('short_description')}"
            for x in items[:5]
        ]
        llm_text = await self.llm_service.generate_response(
            system_prompt=(
                "You are an e-commerce stylist assistant for AIra Styles, a luxury fashion platform. "
                "Be concise, warm, and helpful. Do not hallucinate product details not in the context."
            ),
            user_prompt=query,
            context_blocks=context,
            max_tokens=180,
        )
        if llm_text:
            return llm_text

        first = items[0]
        names = [x.get("product_name", "") for x in items[:3]]
        return (
            f"Here are my top picks for '{query}': {', '.join(names)}. "
            f"Starting from INR {float(first.get('price', 0)):.0f}."
        )
