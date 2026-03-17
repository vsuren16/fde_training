from functools import lru_cache

from app.adapters.chroma_adapter import ChromaVectorStore, NoOpVectorStore
from app.adapters.openai_adapter import OpenAIAdapter
from app.core.config import get_settings
from app.repositories.mongo_repository import AdminRepository, IncidentRepository


@lru_cache
def get_incident_repository() -> IncidentRepository:
    return IncidentRepository()


@lru_cache
def get_admin_repository() -> AdminRepository:
    return AdminRepository()


@lru_cache
def get_vector_store() -> ChromaVectorStore | NoOpVectorStore:
    settings = get_settings()
    if not settings.openai_api_key:
        return NoOpVectorStore()
    try:
        return ChromaVectorStore()
    except Exception:
        return NoOpVectorStore()


@lru_cache
def get_openai_adapter() -> OpenAIAdapter:
    return OpenAIAdapter()
