from typing import List, Optional, Literal
from bson import ObjectId
from app.db.mongodb import get_db
from app.core.config import settings

SortBy = Literal["relevance", "price_asc", "price_desc", "rating_desc"]

def _to_str_id(doc: dict) -> dict:
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc

class ProductRepository:
    @staticmethod
    async def get_by_id(product_id: str) -> Optional[dict]:
        db = get_db()
        col = db[settings.mongo_products_collection]
        query = {"_id": ObjectId(product_id)} if ObjectId.is_valid(product_id) else {"id": product_id}
        doc = await col.find_one(query)
        return _to_str_id(doc) if doc else None

    @staticmethod
    async def list(limit: int = 20, skip: int = 0) -> List[dict]:
        db = get_db()
        col = db[settings.mongo_products_collection]
        cursor = col.find({}, skip=skip, limit=limit)
        docs = await cursor.to_list(length=limit)
        return [_to_str_id(d) for d in docs]

    @staticmethod
    async def search(
        q: str,
        limit: int = 20,
        skip: int = 0,
        brand: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: SortBy = "relevance",
    ) -> List[dict]:
        db = get_db()
        col = db[settings.mongo_products_collection]

        # Base filter
        query: dict = {"$text": {"$search": q}}

        # Optional filters
        if brand:
            query["brand"] = brand
        if category:
            query["category"] = category
        if min_price is not None or max_price is not None:
            price_filter: dict = {}
            if min_price is not None:
                price_filter["$gte"] = min_price
            if max_price is not None:
                price_filter["$lte"] = max_price
            query["price"] = price_filter

        # Projection for text score (only used if relevance sorting)
        projection = {"score": {"$meta": "textScore"}} if sort_by == "relevance" else None

        cursor = col.find(query, projection=projection).skip(skip).limit(limit)

        # Sorting
        if sort_by == "relevance":
            cursor = cursor.sort([("score", {"$meta": "textScore"})])
        elif sort_by == "price_asc":
            cursor = cursor.sort("price", 1)
        elif sort_by == "price_desc":
            cursor = cursor.sort("price", -1)
        elif sort_by == "rating_desc":
            cursor = cursor.sort("rating", -1)

        docs = await cursor.to_list(length=limit)
        return [_to_str_id(d) for d in docs]