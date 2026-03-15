import asyncio
from typing import List, Dict, Any

from app.db.chroma import get_chroma_collection
from app.db.mongodb import get_collection
from app.llm.embeddings import embed_text_async
from app.security.pii import sanitize_text_for_llm

LIST_PROJECTION = {
    "_id": 0,
    "product_id": 1,
    "product_name": 1,
    "short_description": 1,
    "main_image": 1,
    "brand": 1,
    "rating": 1,
    "review_count": 1,
    "price.final_price": 1,
    "price.currency": 1,
    "availability.delivery": 1,
    "availability.pickup": 1,
    "category_name": 1,
    "root_category_name": 1,
}


def _build_retrieval_pack(
    products: List[Dict[str, Any]], max_items: int = 8
) -> List[Dict[str, Any]]:
    """
    Compact payload for LLM grounding (if include_insights=True).
    """
    pack = []
    for p in products[:max_items]:
        pack.append(
            {
                "product_id": p.get("product_id"),
                "product_name": p.get("product_name"),
                "brand": p.get("brand"),
                "category_name": p.get("category_name"),
                "root_category_name": p.get("root_category_name"),
                "final_price": (p.get("price") or {}).get("final_price"),
                "currency": (p.get("price") or {}).get("currency"),
                "rating": p.get("rating"),
                "review_count": p.get("review_count"),
                "short_description": p.get("short_description"),
                "availability": p.get("availability"),
            }
        )
    return pack


async def _chroma_query(query_embedding: List[float], top_k: int):
    """
    Run Chroma sync query in a background thread.
    """
    collection = get_chroma_collection()

    def _run():
        return collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["metadatas", "distances"],  # ✅ FIXED (removed "ids")
        )

    return await asyncio.to_thread(_run)


async def semantic_search_and_hydrate(
    query: str, limit: int = 12
) -> Dict[str, Any]:
    """
    1) Embed query
    2) Query Chroma
    3) Fetch products from Mongo
    4) Preserve ranking order
    """

    sanitized_query = sanitize_text_for_llm(query).sanitized_text or query
    # 1️⃣ Embed query
    qvec = await embed_text_async(sanitized_query)

    # 2️⃣ Query Chroma
    chroma_res = await _chroma_query(qvec, top_k=limit)

    ids = (chroma_res.get("ids") or [[]])[0]
    metas = (chroma_res.get("metadatas") or [[]])[0]
    dists = (chroma_res.get("distances") or [[]])[0]

    ranked_product_ids: List[str] = []

    for i in range(len(ids)):
        pid = None

        if i < len(metas) and isinstance(metas[i], dict):
            pid = metas[i].get("product_id")

        if not pid and i < len(ids):
            pid = ids[i]

        if pid:
            ranked_product_ids.append(str(pid))

    if not ranked_product_ids:
        return {"results": [], "matches": [], "ranked_product_ids": []}

    # 3️⃣ Fetch from Mongo
    col = get_collection("products")

    cursor = col.find(
        {"product_id": {"$in": ranked_product_ids}},
        LIST_PROJECTION,
    )

    docs = []
    async for doc in cursor:
        docs.append(doc)

    # 4️⃣ Preserve ranking
    by_id = {d["product_id"]: d for d in docs if d.get("product_id")}
    results = [by_id[pid] for pid in ranked_product_ids if pid in by_id]

    # Optional match info
    matches = []
    for i, pid in enumerate(ranked_product_ids):
        distance = dists[i] if i < len(dists) else None
        matches.append(
            {
                "product_id": pid,
                "distance": distance,
            }
        )

    return {
        "results": results,
        "matches": matches,
        "ranked_product_ids": ranked_product_ids,
    }


async def search_with_optional_insights(
    query: str, limit: int, include_insights: bool
):
    data = await semantic_search_and_hydrate(query=query, limit=limit)

    results = data["results"]
    retrieval_pack = _build_retrieval_pack(results)

    insights = None
    if include_insights:
        from app.services.insights_service import generate_insights

        insights = await generate_insights(
            {
                "query": sanitize_text_for_llm(query).sanitized_text or query,
                "items": retrieval_pack,
            }
        )

    return {
        "query": query,
        "count": len(results),
        "items": results,
        "matches": data.get("matches", []),
        "retrieval_pack": retrieval_pack,
        "insights": insights,
    }
