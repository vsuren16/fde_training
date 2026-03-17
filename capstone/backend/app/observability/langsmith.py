import os

from langsmith import traceable

from app.core.config import get_settings


def traced(run_type: str, name: str):
    return traceable(run_type=run_type, name=name)


def configure_langsmith() -> bool:
    settings = get_settings()
    if not settings.langsmith_api_key or not settings.langsmith_tracing:
        return False

    os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
    os.environ["LANGSMITH_TRACING"] = "true"
    return True
