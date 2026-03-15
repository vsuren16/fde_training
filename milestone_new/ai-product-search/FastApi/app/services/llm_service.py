from __future__ import annotations

import logging
from typing import Iterable

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self) -> None:
        self.client = None
        if settings.openai_api_key:
            self.client = AsyncOpenAI(
                api_key=settings.openai_api_key,
                timeout=settings.request_timeout_seconds,
                max_retries=2,
            )
        self.model_version = f"openai:{settings.chat_model}" if self.client else "rule:fallback-v1"

    async def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        context_blocks: Iterable[str],
        max_tokens: int = 220,
    ) -> str | None:
        if not self.client:
            return None

        context_text = "\n\n".join(f"- {x}" for x in context_blocks if x)
        prompt = (
            "Use ONLY the provided context. If context is insufficient, reply exactly: "
            "'I do not have enough relevant information to answer that accurately right now.'\n\n"
            f"Context:\n{context_text}\n\nUser Query:\n{user_prompt}"
        )

        # Use chat.completions.create — works on all openai SDK versions (>=1.0)
        # client.responses.create() only exists in openai>=1.66 (Responses API)
        try:
            response = await self.client.chat.completions.create(
                model=settings.chat_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=0.4,
            )
            text = (response.choices[0].message.content or "").strip()
            return text or None
        except Exception as exc:
            logger.warning("llm_generation_failed", extra={"model": settings.chat_model, "reason": str(exc)})
            return None

    async def close(self) -> None:
        if self.client:
            await self.client.close()
