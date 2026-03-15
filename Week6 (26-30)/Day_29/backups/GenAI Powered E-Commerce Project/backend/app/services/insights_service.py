import json
from typing import List

from app.repositories.product_repo import ProductRepository
from app.schemas.insights import InsightRequest, InsightResponse, RecommendedProduct
from app.llm.openai_client import get_openai_client
from app.core.config import settings

SYSTEM_PROMPT = """You are a product analyst for an e-commerce site.
You MUST ground your answer only in the provided product catalog items.
If the catalog data is insufficient to answer, say what is missing and avoid guessing.
Return strictly valid JSON matching the given schema.
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "highlights": {"type": "array", "items": {"type": "string"}},
        "recommended_products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": ["product_id", "reason"],
                "additionalProperties": False
            }
        },
        "citations": {"type": "array", "items": {"type": "string"}},
        "safety_notes": {"type": ["string", "null"]}
    },
    "required": ["answer", "highlights", "recommended_products", "citations", "safety_notes"],
    "additionalProperties": False
}

def _compact_products(products: List[dict]) -> List[dict]:
    # Keep only fields the model needs; reduces token use and leakage risk
    out = []
    for p in products:
        out.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "description": p.get("description"),
            "brand": p.get("brand"),
            "category": p.get("category"),
            "price": p.get("price"),
            "rating": p.get("rating"),
            "tags": p.get("tags", []),
        })
    return out

async def generate_insights(req: InsightRequest) -> InsightResponse:
    # Retrieve products first (grounding)
    products = await ProductRepository.search(
        q=req.query,
        limit=req.limit,
        skip=0,
        brand=req.brand,
        category=req.category,
        min_price=req.min_price,
        max_price=req.max_price,
        sort_by=req.sort_by,  # your repo supports this
    )

    catalog = _compact_products(products)

    client = get_openai_client()

    user_payload = {
        "user_query": req.query,
        "catalog_items": catalog,
        "instructions": (
            "Choose up to 3 recommended products from catalog_items. "
            "Citations must be the product ids you used. "
            "Do not cite products not present in catalog_items."
        )
    }

    # Use response_format=json_schema to force strict JSON
    resp = await client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(user_payload)}
        ],
        response_format={"type": "json_schema", "json_schema": {"name": "insight", "schema": OUTPUT_SCHEMA}},
    )

    text = resp.output_text
    data = json.loads(text)

    return InsightResponse(
        answer=data["answer"],
        highlights=data["highlights"],
        recommended_products=[RecommendedProduct(**rp) for rp in data["recommended_products"]],
        citations=data["citations"],
        safety_notes=data.get("safety_notes"),
    )