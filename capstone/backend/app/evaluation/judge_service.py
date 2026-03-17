from __future__ import annotations

from dataclasses import dataclass

from app.adapters.openai_adapter import OpenAIAdapter
from app.observability.langsmith import traced
from app.services.keyword_search_service import tokenize


@dataclass
class JudgeVerdict:
    status: str
    score: float
    reason: str
    approved: bool


class JudgeService:
    def __init__(self, openai_adapter: OpenAIAdapter) -> None:
        self.openai_adapter = openai_adapter

    @traced(run_type="chain", name="llm_judge")
    def evaluate(
        self,
        query: str,
        incidents: list[dict],
        answer: str,
        use_llm: bool = True,
    ) -> JudgeVerdict:
        if not incidents:
            return JudgeVerdict(
                status="blocked",
                score=0.0,
                reason="No incidents were retrieved, so the answer cannot be grounded.",
                approved=False,
            )

        try:
            if use_llm and self.openai_adapter.enabled:
                return self.openai_adapter.judge_response(query, incidents, answer)
        except Exception:
            pass

        return self._heuristic_verdict(query, incidents, answer)

    def _heuristic_verdict(self, query: str, incidents: list[dict], answer: str) -> JudgeVerdict:
        query_tokens = set(tokenize(query))
        answer_tokens = set(tokenize(answer))
        evidence_tokens = set()
        for incident in incidents:
            evidence_tokens.update(tokenize(str(incident.get("title") or "")))
            evidence_tokens.update(tokenize(str(incident.get("incident_text") or "")))
            evidence_tokens.update(tokenize(str(incident.get("description") or "")))
            evidence_tokens.update(tokenize(str(incident.get("resolution_notes") or "")))
            evidence_tokens.update(tokenize(str(incident.get("category") or "")))
            evidence_tokens.update(tokenize(str(incident.get("team") or "")))

        query_overlap = len(query_tokens & evidence_tokens) / max(len(query_tokens), 1)
        answer_overlap = len(answer_tokens & evidence_tokens) / max(len(answer_tokens), 1)
        score = round((0.45 * query_overlap) + (0.55 * answer_overlap), 4)

        if answer_overlap < 0.12:
            return JudgeVerdict(
                status="blocked",
                score=score,
                reason="The answer content does not sufficiently overlap with retrieved evidence.",
                approved=False,
            )
        if score >= 0.24:
            return JudgeVerdict(
                status="approved",
                score=score,
                reason="The response substantially overlaps with retrieved evidence.",
                approved=True,
            )
        if score >= 0.14:
            return JudgeVerdict(
                status="degraded",
                score=score,
                reason="The response is only partially grounded in retrieved evidence.",
                approved=False,
            )
        return JudgeVerdict(
            status="blocked",
            score=score,
            reason="The response does not appear sufficiently grounded in retrieved evidence.",
            approved=False,
        )
