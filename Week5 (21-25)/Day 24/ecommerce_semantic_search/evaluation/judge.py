from __future__ import annotations

import asyncio
import json

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_JUDGE_MODEL, OPENAI_TIMEOUT_SECONDS
from generation.prompt_builder import build_judge_messages


class Judge:
    def __init__(self, model: str = OPENAI_JUDGE_MODEL):
        self.model = model
        self.client = OpenAI(api_key=OPENAI_API_KEY, timeout=OPENAI_TIMEOUT_SECONDS)

    @staticmethod
    def _validate(payload: dict) -> dict:
        out = {
            "relevance": int(payload.get("relevance", 1)),
            "faithfulness": int(payload.get("faithfulness", 1)),
            "completeness": int(payload.get("completeness", 1)),
            "overall_score": float(payload.get("overall_score", 1.0)),
            "reasoning": str(payload.get("reasoning", "")),
        }
        for key in ["relevance", "faithfulness", "completeness"]:
            out[key] = min(5, max(1, out[key]))
        out["overall_score"] = round((out["relevance"] + out["faithfulness"] + out["completeness"]) / 3, 3)
        return out

    async def evaluate(self, query: str, ranked_products: list[dict], llm_explanation: str) -> dict:
        messages = build_judge_messages(query, ranked_products, llm_explanation)

        def _call() -> dict:
            resp = self.client.chat.completions.create(
                model=self.model,
                temperature=0,
                messages=messages,
                response_format={"type": "json_object"},
            )
            raw = resp.choices[0].message.content or "{}"
            data = json.loads(raw)
            return self._validate(data)

        try:
            return await asyncio.wait_for(asyncio.to_thread(_call), timeout=OPENAI_TIMEOUT_SECONDS + 5)
        except Exception as ex:
            return {
                "relevance": 1,
                "faithfulness": 1,
                "completeness": 1,
                "overall_score": 1.0,
                "reasoning": f"Judge unavailable: {ex}",
            }
