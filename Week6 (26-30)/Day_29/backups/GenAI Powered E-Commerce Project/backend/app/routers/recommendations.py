from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.db.mongodb import get_collection  # use your existing dependency
from app.recommendations.review_similarity_service import get_review_based_recommendations

router = APIRouter(tags=["recommendations"])

class RecommendationsRequest(BaseModel):
    product_id: str = Field(..., description="Seed product id")
    k: int = Field(8, ge=1, le=20)
    same_category: bool = True

class RecommendationItem(BaseModel):
    product_id: str
    title: Optional[str] = None
    category: Optional[str] = None
    price_final: Optional[float] = None
    main_image: Optional[str] = None
    images: list[str] = []
    score: float

@router.post("/recommendations", response_model=list[RecommendationItem])
async def recommendations(req: RecommendationsRequest, products_col=Depends(get_collection)):
    items = await get_review_based_recommendations(
        products_col=products_col,
        product_id=req.product_id,
        k=req.k,
        same_category=req.same_category,
    )
    if not items:
        raise HTTPException(
            status_code=404,
            detail="No recommendations found (seed missing or not indexed yet).",
        )
    return items