from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.recommendations.schemas import RecommendRequest, RecommendResponse
from app.infrastructure.db.session import get_db_session

router = APIRouter()


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(
    payload: RecommendRequest,
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> RecommendResponse:
    return await request.app.state.container.recommendation_service.recommend(payload, db)
