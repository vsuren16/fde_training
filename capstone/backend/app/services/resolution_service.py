from __future__ import annotations

from app.adapters.openai_adapter import OpenAIAdapter
from app.observability.langsmith import traced


class ResolutionService:
    def __init__(self, openai_adapter: OpenAIAdapter) -> None:
        self.openai_adapter = openai_adapter

    @traced(run_type="chain", name="resolution_summary")
    def summarize(self, query: str, incidents: list[dict]) -> tuple[str, bool]:
        if not incidents:
            return (
                "No similar incidents were found. Refine the query or relax metadata filters.",
                True,
            )
        try:
            summary = self.openai_adapter.summarize_resolution(query, incidents)
            return summary, False
        except Exception:
            lead = incidents[0]
            fallback = (
                f"Similar incidents suggest starting with {lead.get('resolution_notes', '').strip()} "
                "Treat this as guidance grounded in retrieved historical patterns."
            )
            return fallback.strip(), True

    @traced(run_type="chain", name="llm_best_effort_resolution")
    def best_effort_guidance(self, query: str) -> tuple[str, bool]:
        try:
            guidance = self.openai_adapter.generate_best_effort_resolution(query)
            return guidance, True
        except Exception:
            return (
                "The internal knowledge base did not return sufficiently relevant historical "
                "evidence for this query, and the fallback LLM guidance path was unavailable. "
                "Refine the incident description or escalate to support for manual triage.",
                False,
            )
