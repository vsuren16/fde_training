from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.observability.langsmith import configure_langsmith
from app.repositories.mongo_repository import get_mongo_client
from app.observability.logging import configure_logging, get_logger
from app.services.runtime_state import get_search_service


settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    langsmith_enabled = configure_langsmith()
    logger.info(
        "application_starting",
        extra={
            "app_name": settings.app_name,
            "environment": settings.app_env,
            "langsmith_enabled": langsmith_enabled,
        },
    )
    try:
        get_mongo_client().admin.command("ping")
        loaded = get_search_service().warm()
        logger.info("application_warmed", extra={"loaded_incidents": loaded})
    except Exception as exc:
        logger.warning("application_warmup_skipped", extra={"error": str(exc)})
    yield
    logger.info("application_stopping", extra={"app_name": settings.app_name})


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.api_prefix)
