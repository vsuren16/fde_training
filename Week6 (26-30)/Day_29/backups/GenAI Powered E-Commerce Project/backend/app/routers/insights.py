from fastapi import APIRouter, HTTPException
from app.core.openai_client import get_openai_client
from app.schemas.insights import InsightsRequest, InsightsResponse
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
    client = get_openai_client()

    # Keep prompt compact and deterministic
    user_content = {
        "query": payload.query,
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
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": json.dumps(user_content)},
            ],
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        return InsightsResponse(**data)
    except Exception as e:
        # Return a stable error for frontend
        raise HTTPException(
            status_code=500,
            detail={"code": "OPENAI_INSIGHTS_FAILED", "message": str(e)},
        )