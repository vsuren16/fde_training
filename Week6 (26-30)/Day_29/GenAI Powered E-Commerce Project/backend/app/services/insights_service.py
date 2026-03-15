import json
from typing import Any, Dict, List

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from app.llm.openai_client import get_openai_client
from app.security.pii import sanitize_text_for_llm

SYSTEM_PROMPT = """You are a product analyst for an e-commerce site.
You MUST ground your answer only in the provided product catalog items.
If the catalog data is insufficient to answer, say what is missing and avoid guessing.
Return strictly valid JSON matching the given schema.
"""

class RecommendedProduct(BaseModel):
    product_id: str
    reason: str


class InsightPayload(BaseModel):
    answer: str
    highlights: List[str] = Field(default_factory=list)
    recommended_products: List[RecommendedProduct] = Field(default_factory=list)
    citations: List[str] = Field(default_factory=list)
    safety_notes: str | None = None

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

async def generate_insights(payload: Dict[str, Any]) -> Dict[str, Any]:
    query = str(payload.get("query") or "").strip()
    catalog_items = payload.get("items") or []
    catalog = _compact_products(catalog_items if isinstance(catalog_items, list) else [])

    client = get_openai_client().with_structured_output(InsightPayload)

    user_payload = {
        "user_query": sanitize_text_for_llm(query).sanitized_text or query,
        "catalog_items": catalog,
        "instructions": (
            "Choose up to 3 recommended products from catalog_items. "
            "Citations must be the product ids you used. "
            "Do not cite products not present in catalog_items."
        )
    }

    resp = await client.ainvoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=json.dumps(user_payload)),
        ]
    )
    data = resp.model_dump()
    return {
        "answer": data["answer"],
        "highlights": data["highlights"],
        "recommended_products": data["recommended_products"],
        "citations": data["citations"],
        "safety_notes": data.get("safety_notes"),
    }
