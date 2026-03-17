from pathlib import Path

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import FileResponse

from app.core.config import get_settings
from app.core.container import get_openai_adapter, get_vector_store
from app.schemas.admin import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminObservabilityResponse,
    AdminSignupRequest,
    AdminSignupResponse,
)
from app.services.admin_auth_service import AdminAuthService
from app.services.integration_status_service import IntegrationStatusService
from app.services.runtime_state import get_keyword_search_service, get_search_diagnostics_service


router = APIRouter()


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    return authorization.split(" ", maxsplit=1)[1]


@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(payload: AdminLoginRequest) -> AdminLoginResponse:
    token, expires_in = AdminAuthService().login(payload.username, payload.password)
    return AdminLoginResponse(access_token=token, expires_in=expires_in)


@router.post("/signup", response_model=AdminSignupResponse)
async def admin_signup(
    payload: AdminSignupRequest,
    authorization: str | None = Header(default=None),
) -> AdminSignupResponse:
    auth_service = AdminAuthService()
    if auth_service.has_persisted_admins():
        token = _extract_bearer_token(authorization)
        auth_service.verify_token(token)
    created = auth_service.signup(payload.username, payload.password)
    if not created:
        raise HTTPException(status_code=409, detail="admin username already exists")
    return AdminSignupResponse(status="ok", created=True)


@router.get("/observability", response_model=AdminObservabilityResponse)
async def admin_observability(
    authorization: str | None = Header(default=None),
) -> AdminObservabilityResponse:
    token = _extract_bearer_token(authorization)
    AdminAuthService().verify_token(token)

    settings = get_settings()
    vector_store = get_vector_store()
    status_service = IntegrationStatusService(get_openai_adapter(), vector_store)
    mongo_status = status_service.mongo_status()
    langsmith_status = status_service.langsmith_status()
    chroma_status = status_service.chroma_status()
    openai_status = status_service.openai_status()

    return AdminObservabilityResponse(
        tracing_enabled=bool(settings.langsmith_tracing and settings.langsmith_api_key),
        langsmith_project=settings.langsmith_project or None,
        langsmith_project_url=settings.langsmith_project_url or None,
        mongo=mongo_status,
        langsmith=langsmith_status,
        chroma=chroma_status,
        openai=openai_status,
        persisted_admins=AdminAuthService().has_persisted_admins(),
        vector_store_count=vector_store.count(),
        keyword_index_loaded=get_keyword_search_service().is_loaded(),
        log_file_path=str((settings.log_dir + "/" + settings.log_file_name).replace("\\", "/")),
        last_search_diagnostics=get_search_diagnostics_service().get_latest(),
    )


@router.get("/logs/download")
async def admin_download_logs(
    authorization: str | None = Header(default=None),
) -> FileResponse:
    token = _extract_bearer_token(authorization)
    AdminAuthService().verify_token(token)
    settings = get_settings()
    log_path = Path(settings.log_dir) / settings.log_file_name
    if not log_path.exists():
        raise HTTPException(status_code=404, detail="log file not found")
    return FileResponse(
        path=log_path,
        media_type="text/plain",
        filename=settings.log_file_name,
    )
