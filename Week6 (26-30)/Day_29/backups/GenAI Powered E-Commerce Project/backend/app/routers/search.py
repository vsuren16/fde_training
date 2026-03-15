import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.search_service import search_with_optional_insights

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Search"])

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=12, ge=1, le=50)
    include_insights: bool = False

@router.post("/search")
async def search(req: SearchRequest):
    try:
        return await search_with_optional_insights(
            query=req.query,
            limit=req.limit,
            include_insights=req.include_insights,
        )
    except Exception as e:
        logger.exception("POST /search failed")
        # show real error while developing (remove in production)
        raise HTTPException(status_code=500, detail=str(e))