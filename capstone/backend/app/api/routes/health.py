from fastapi import APIRouter

from app.core.container import get_vector_store
from app.repositories.mongo_repository import get_mongo_client
from app.schemas.health import HealthResponse


router = APIRouter()


@router.get("/health/live", response_model=HealthResponse)
async def liveness_probe() -> HealthResponse:
    return HealthResponse(status="ok", service="backend", detail="service is live")


@router.get("/health/ready", response_model=HealthResponse)
async def readiness_probe() -> HealthResponse:
    try:
        get_mongo_client().admin.command("ping")
        vector_count = get_vector_store().count()
        return HealthResponse(
            status="ok",
            service="backend",
            detail=f"service is ready; vector_count={vector_count}",
        )
    except Exception as exc:
        return HealthResponse(
            status="degraded",
            service="backend",
            detail=f"dependency check failed: {exc}",
        )
