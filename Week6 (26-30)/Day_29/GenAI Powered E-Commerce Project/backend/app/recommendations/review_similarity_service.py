from typing import Any, Optional

from app.db.chroma_client import get_reviews_collection
from app.llm.embeddings import embed_text
from app.recommendations.review_text_builder import build_review_text_agg


def _get_pid(doc: dict[str, Any]) -> str:
    if doc.get("product_id"):
        return str(doc["product_id"])
    return str(doc["_id"])


async def get_review_based_recommendations(
    products_col,
    product_id: str,
    k: int = 8,
    same_category: bool = True,
) -> list[dict[str, Any]]:
    """
    1) Load seed product from Mongo
    2) Build review_text_agg and embed it
    3) Query Chroma walmart_reviews
    4) Hydrate candidates from Mongo and return cards + score
    """

    # 1) Seed product lookup (support either product_id or _id stored as string)
    seed = await products_col.find_one(
        {"$or": [{"product_id": product_id}, {"_id": product_id}]},
        {
            "_id": 1,
            "product_id": 1,
            "category": 1,
            "title": 1,
            "name": 1,
            "reviews": 1,
            "review_summary": 1,
            "reviews_summary": 1,
            "description": 1,
            "short_description": 1,
        },
    )
    if not seed:
        return []

    seed_pid = _get_pid(seed)
    seed_category = seed.get("category")

    # 2) Build + embed seed text
    seed_text = build_review_text_agg(seed)
    seed_emb = embed_text(seed_text)
    if not seed_emb:
        return []

    # 3) Query Chroma
    reviews_coll = get_reviews_collection()

    # request more than k so we can drop self + filter
    n = min(max(k + 8, k + 1), 30)

    chroma_res = reviews_coll.query(
        query_embeddings=[seed_emb],
        n_results=n,
        include=["ids", "distances", "metadatas"],
    )

    ids = chroma_res.get("ids", [[]])[0]
    distances = chroma_res.get("distances", [[]])[0]
    metadatas = chroma_res.get("metadatas", [[]])[0]

    # 4) Filter out self and (optionally) other categories
    candidates: list[tuple[str, float]] = []
    for pid, dist, meta in zip(ids, distances, metadatas):
        pid = str(pid)
        if pid == seed_pid:
            continue
        if same_category and seed_category and meta and meta.get("category") and meta.get("category") != seed_category:
            continue
        candidates.append((pid, float(dist)))

    candidates = candidates[:k]
    if not candidates:
        return []

    cand_ids = [c[0] for c in candidates]

    # 5) Hydrate from Mongo
    mongo_docs = await products_col.find(
        {"$or": [{"product_id": {"$in": cand_ids}}, {"_id": {"$in": cand_ids}}]},
        {
            "_id": 1,
            "product_id": 1,
            "title": 1,
            "name": 1,
            "category": 1,
            "price": 1,
            "main_image": 1,
            "images": 1,
        },
    ).to_list(length=len(cand_ids))

    doc_map = {_get_pid(d): d for d in mongo_docs}

    # 6) Build response list
    out: list[dict[str, Any]] = []
    for pid, dist in candidates:
        p = doc_map.get(pid)
        if not p:
            continue

        # Convert cosine distance to a simple "higher is better" score
        score = max(0.0, 1.0 - dist)

        out.append(
            {
                "product_id": pid,
                "title": p.get("title") or p.get("name"),
                "category": p.get("category"),
                "price_final": (p.get("price") or {}).get("final_price"),
                "main_image": p.get("main_image"),
                "images": p.get("images") or [],
                "score": float(score),
            }
        )

    out.sort(key=lambda x: x["score"], reverse=True)
    return out