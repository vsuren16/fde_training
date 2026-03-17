from __future__ import annotations


class TokenOptimizationService:
    def select_evidence(self, incidents: list[dict], max_items: int = 3, max_chars: int = 2200) -> list[dict]:
        selected: list[dict] = []
        budget = 0
        for incident in incidents[:max_items]:
            compact = {
                "incident_id": incident.get("incident_id"),
                "title": incident.get("title"),
                "category": incident.get("category"),
                "status": incident.get("status"),
                "team": incident.get("team"),
                "description": incident.get("description"),
                "incident_text": incident.get("incident_text"),
                "resolution_notes": incident.get("resolution_notes"),
            }
            size = len(str(compact))
            if budget + size > max_chars and selected:
                break
            selected.append(compact)
            budget += size
        return selected
