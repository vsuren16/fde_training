import asyncio
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.db.chroma_client import get_reviews_collection
from app.llm.embeddings import embed_text
from app.recommendations.review_text_builder import build_review_text_agg


def _pid(p: dict[str, Any]) -> str:
    # Prefer explicit product_id; otherwise use _id
    if p.get("product_id"):
        return str(p["product_id"])
    return str(p["_id"])


async def main():
    mongo = AsyncIOMotorClient(settings.mongo_uri)
    col = mongo[settings.mongo_db][settings.mongo_products_collection]

    reviews_coll = get_reviews_collection()

    cursor = col.find(
        {},
        {
            "_id": 1,
            "product_id": 1,
            "title": 1,
            "name": 1,
            "description": 1,
            "short_description": 1,
            "reviews": 1,
            "review_summary": 1,
            "reviews_summary": 1,
            "category": 1,
            "brand": 1,
            "price": 1,
        },
    ).limit(20)

    ids, embs, docs, metas = [], [], [], []

    async for p in cursor:
        pid = _pid(p)
        review_text = build_review_text_agg(p)

        if not review_text.strip():
            print(f"SKIP (no text): {pid}")
            continue

        emb = embed_text(review_text)
        if not emb:
            print(f"SKIP (no embedding): {pid}")
            continue

        meta = {
            "product_id": pid,
            "category": p.get("category"),
            "brand": p.get("brand"),
        }

        # optional price
        try:
            price = (p.get("price") or {}).get("final_price")
            if price is not None:
                meta["price_final"] = float(price)
        except Exception:
            pass

        ids.append(pid)
        embs.append(emb)
        docs.append(review_text)
        metas.append(meta)

        print(f"READY: {pid} (chars={len(review_text)})")

    if not ids:
        print("Nothing to index.")
        return

    # IMPORTANT: we pass embeddings explicitly (no dependency on Chroma embedding function)
    reviews_coll.upsert(ids=ids, embeddings=embs, documents=docs, metadatas=metas)
    print(f"Indexed {len(ids)} items into collection: {reviews_coll.name}")


if __name__ == "__main__":
    asyncio.run(main())