from openai import OpenAI

from backend.app.core.config import settings


def get_openai_client() -> OpenAI | None:
    if not settings.openai_api_key:
        return None
    return OpenAI(api_key=settings.openai_api_key)
