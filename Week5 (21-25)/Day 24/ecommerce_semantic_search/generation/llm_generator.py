from __future__ import annotations

import asyncio

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TIMEOUT_SECONDS
from generation.prompt_builder import build_generation_messages


class LLMGenerator:
    def __init__(self, model: str = OPENAI_MODEL):
        self.model = model
        self.client = OpenAI(api_key=OPENAI_API_KEY, timeout=OPENAI_TIMEOUT_SECONDS)

    async def generate(self, query: str, ranked_products: list[dict]) -> str:
        messages = build_generation_messages(query, ranked_products)

        def _call() -> str:
            resp = self.client.chat.completions.create(
                model=self.model,
                temperature=0.2,
                messages=messages,
            )
            return resp.choices[0].message.content or ""

        try:
            return await asyncio.wait_for(asyncio.to_thread(_call), timeout=OPENAI_TIMEOUT_SECONDS + 5)
        except Exception as ex:
            return f"LLM generation unavailable: {ex}"
