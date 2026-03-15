from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage, SystemMessage

from app.core.openai_client import get_openai_client
from app.schemas.insights import InsightsRequest, InsightsResponse
from app.security.pii import sanitize_text_for_llm
import json

router = APIRouter(prefix="/insights", tags=["Insights"])

SYSTEM = """You are an e-commerce shopping assistant.
Rules:
- Only use the provided product snippets. Do NOT invent specs, prices, or features.
- If info is missing, say it's missing.
- Output must be valid JSON matching the required schema.
"""

@router.post("", response_model=InsightsResponse)
def generate_insights(payload: InsightsRequest) -> InsightsResponse:
    client = get_openai_client().with_structured_output(InsightsResponse)

    # Keep prompt compact and deterministic
    user_content = {
        "query": sanitize_text_for_llm(payload.query).sanitized_text or payload.query,
        "products": [p.model_dump() for p in payload.products][:50],
        "max_items": payload.max_items,
        "required_json_schema": {
            "answer": "string",
            "items": [
                {
                    "product_id": "string",
                    "title": "string",
                    "best_for": ["string"],
                    "pros": ["string"],
                    "cons": ["string"],
                    "confidence": "low|medium|high"
                }
            ],
            "safety_notes": ["string"]
        }
    }

    try:
        resp = client.invoke(
            [
                SystemMessage(content=SYSTEM),
                HumanMessage(content=json.dumps(user_content)),
            ]
        )
        return resp
    except Exception as e:
        # Return a stable error for frontend
        raise HTTPException(
            status_code=500,
            detail={"code": "OPENAI_INSIGHTS_FAILED", "message": str(e)},
        )
