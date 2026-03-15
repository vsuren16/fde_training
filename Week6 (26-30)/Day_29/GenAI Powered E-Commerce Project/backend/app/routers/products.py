from typing import Optional, Dict, Any, List, Literal
from fastapi import APIRouter, HTTPException, Query

from app.db.mongodb import get_collection

router = APIRouter(tags=["Products"])

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
}

SortBy = Literal[
    "relevance",        # default (no explicit sort; good for regex demo)
    "price_asc",
    "price_desc",
    "rating_desc",
    "review_count_desc",
]

def _build_sort(sort_by: SortBy):
    if sort_by == "price_asc":
        return [("price.final_price", 1)]
    if sort_by == "price_desc":
        return [("price.final_price", -1)]
    if sort_by == "rating_desc":
        return [("rating", -1)]
    if sort_by == "review_count_desc":
        return [("review_count", -1)]
    # relevance: for now just don't sort (Mongo natural / index order)
    return None


async def _fetch_products(
    q: Optional[str],
    limit: int,
    skip: int,
    category: Optional[str] = None,
    root_category: Optional[str] = None,
    brand: Optional[str] = None,
    sort_by: SortBy = "relevance",
) -> Dict[str, Any]:
    col = get_collection("products")

    mongo_filter: Dict[str, Any] = {}
    if category:
        mongo_filter["category_name"] = category
    if root_category:
        mongo_filter["root_category_name"] = root_category
    if brand:
        mongo_filter["brand"] = brand

    if q:
        mongo_filter["$or"] = [
            {"product_name": {"$regex": q, "$options": "i"}},
            {"brand": {"$regex": q, "$options": "i"}},
            {"category_name": {"$regex": q, "$options": "i"}},
            {"root_category_name": {"$regex": q, "$options": "i"}},
            {"short_description": {"$regex": q, "$options": "i"}},
        ]

    cursor = (
        col.find(mongo_filter, LIST_PROJECTION)
        .skip(skip)
        .limit(limit)
    )

    sort_spec = _build_sort(sort_by)
    if sort_spec:
        cursor = cursor.sort(sort_spec)

    items: List[dict] = []
    async for doc in cursor:
        items.append(doc)

    return {
        "count": len(items),
        "items": items,
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
        "q": q,
    }


@router.get("/products")
async def list_products(
    q: Optional[str] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    category: Optional[str] = Query(default=None),
    root_category: Optional[str] = Query(default=None),
    brand: Optional[str] = Query(default=None),
    sort_by: SortBy = Query(default="relevance"),
):
    return await _fetch_products(
        q=q,
        limit=limit,
        skip=skip,
        category=category,
        root_category=root_category,
        brand=brand,
        sort_by=sort_by,
    )


# ✅ Alias endpoint so /products/search works for your current calls
@router.get("/products/search")
async def search_products(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    sort_by: SortBy = Query(default="relevance"),
):
    return await _fetch_products(q=q, limit=limit, skip=skip, sort_by=sort_by)


@router.get("/products/{product_id}")
async def product_detail(product_id: str) -> Dict[str, Any]:
    col = get_collection("products")

    doc = await col.find_one({"product_id": product_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")

    # ensure carousel list exists
    if "images" not in doc or not isinstance(doc["images"], list):
        main_image = doc.get("main_image")
        doc["images"] = [main_image] if main_image else []

    return doc