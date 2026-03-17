from app.core.config import get_settings


def tracing_is_enabled() -> bool:
    settings = get_settings()
    return bool(settings.langsmith_tracing and settings.langsmith_api_key)
