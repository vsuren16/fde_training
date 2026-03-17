from __future__ import annotations


class TriageService:
    def classify_priority(self, query: str, incidents: list[dict]) -> int:
        text = query.lower()
        if any(term in text for term in ["outage", "down", "denied", "cannot access"]):
            return 2
        if any(term in text for term in ["timeout", "slow", "latency", "freeze"]):
            return 3

        priorities = [item.get("priority") for item in incidents if item.get("priority")]
        if priorities:
            return int(min(priorities))
        return 4
