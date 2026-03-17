from __future__ import annotations

import json
from typing import Any

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings


class OpenAIAdapter:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.embedding_model = settings.openai_embedding_model
        self.chat_model = settings.openai_chat_model
        self.enabled = bool(settings.openai_api_key)
        self.client = (
            OpenAI(
                api_key=settings.openai_api_key,
                timeout=settings.openai_timeout_seconds,
                max_retries=1,
            )
            if self.enabled
            else None
        )

    @retry(wait=wait_exponential(min=1, max=3), stop=stop_after_attempt(2), reraise=True)
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not self.enabled or self.client is None:
            raise RuntimeError("openai_api_key is not configured")
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    def check_connectivity(self) -> None:
        if not self.enabled or self.client is None:
            raise RuntimeError("openai_api_key is not configured")
        self.client.models.list()

    @retry(wait=wait_exponential(min=1, max=2), stop=stop_after_attempt(1), reraise=True)
    def summarize_resolution(
        self,
        query: str,
        incidents: list[dict[str, Any]],
    ) -> str:
        if not self.enabled or self.client is None:
            raise RuntimeError("openai_api_key is not configured")

        evidence = "\n".join(
            [
                (
                    f"Incident ID: {incident['incident_id']}\n"
                    f"Title: {incident.get('title', '')}\n"
                    f"Category: {incident.get('category', '')}\n"
                    f"Incident Text: {incident['incident_text']}\n"
                    f"Description: {incident.get('description', '')}\n"
                    f"Resolution Notes: {incident.get('resolution_notes', '')}\n"
                )
                for incident in incidents
            ]
        )
        response = self.client.responses.create(
            model=self.chat_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are an incident support assistant. Use only the supplied "
                        "incident evidence. Summarize likely troubleshooting steps in 4 "
                        "sentences maximum and avoid claiming certainty."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Query:\n{query}\n\nEvidence:\n{evidence}",
                },
            ],
        )
        return response.output_text.strip()

    @retry(wait=wait_exponential(min=1, max=2), stop=stop_after_attempt(1), reraise=True)
    def generate_best_effort_resolution(self, query: str) -> str:
        if not self.enabled or self.client is None:
            raise RuntimeError("openai_api_key is not configured")

        response = self.client.responses.create(
            model=self.chat_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are an experienced IT incident response engineer. The internal "
                        "knowledge base did not contain sufficiently relevant historical "
                        "matches. Provide cautious, practical troubleshooting guidance for "
                        "the user's issue in 5 sentences maximum. Avoid claiming you verified "
                        "facts from internal evidence. Include validation-oriented next steps."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Incident query:\n{query}",
                },
            ],
        )
        return response.output_text.strip()

    @retry(wait=wait_exponential(min=1, max=2), stop=stop_after_attempt(1), reraise=True)
    def judge_response(
        self,
        query: str,
        incidents: list[dict[str, Any]],
        answer: str,
    ):
        if not self.enabled or self.client is None:
            raise RuntimeError("openai_api_key is not configured")

        evidence = "\n".join(
            [
                (
                    f"Incident ID: {incident['incident_id']}\n"
                    f"Title: {incident.get('title', '')}\n"
                    f"Category: {incident.get('category', '')}\n"
                    f"Incident Text: {incident['incident_text']}\n"
                    f"Description: {incident.get('description', '')}\n"
                    f"Resolution Notes: {incident.get('resolution_notes', '')}\n"
                )
                for incident in incidents
            ]
        )
        response = self.client.responses.create(
            model=self.chat_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict judge for RAG answers. Score whether the answer "
                        "is grounded in the supplied evidence and relevant to the user query. "
                        "Return strict JSON with keys: status, score, reason, approved. "
                        "status must be one of approved, degraded, blocked. score must be between 0 and 1."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Query:\n{query}\n\nAnswer:\n{answer}\n\nEvidence:\n{evidence}\n\n"
                        "Judge whether the answer is relevant and non-hallucinated."
                    ),
                },
            ],
        )
        payload = json.loads(response.output_text)
        from app.evaluation.judge_service import JudgeVerdict

        return JudgeVerdict(
            status=str(payload["status"]),
            score=float(payload["score"]),
            reason=str(payload["reason"]),
            approved=bool(payload["approved"]),
        )
