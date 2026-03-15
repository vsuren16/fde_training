from openai import OpenAI
from app.core.config import settings

_client = OpenAI(api_key=settings.openai_api_key)

def embed_text(text: str) -> list[float]:
    """
    Returns a single embedding vector for the input text.
    Defensive: empty input => empty list.
    """
    text = (text or "").strip()
    if not text:
        return []

    # clamp to avoid extreme payloads
    text = text[:12000]

    resp = _client.embeddings.create(
        model=settings.openai_embed_model,
        input=text
    )
    return resp.data[0].embedding