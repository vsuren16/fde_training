from __future__ import annotations

from app.adapters.openai_adapter import OpenAIAdapter


class RootCauseService:
    def __init__(self, openai_adapter: OpenAIAdapter) -> None:
        self.openai_adapter = openai_adapter

    def summarize(self, query: str, incidents: list[dict], handoff_path: list[str]) -> str | None:
        if not incidents:
            return None
        top = incidents[0]
        return (
            f"Probable root cause for '{query}' aligns with the {top.get('category', 'unknown')} incident pattern "
            f"owned by {top.get('team', 'the current support team')}. "
            f"The recommended specialist path is {' -> '.join(handoff_path)}."
        )
