from __future__ import annotations

from datetime import datetime


class RerankingService:
    def rerank(self, incidents: list[dict], score_lookup: dict[str, float]) -> list[dict]:
        ranked: list[tuple[float, dict]] = []
        for incident in incidents:
            base = score_lookup.get(incident["incident_id"], 0.0)
            recency = self._recency_score(
                incident.get("updated_at"),
                incident.get("closed_at"),
                incident.get("created_at"),
            )
            success = self._resolution_success_score(incident.get("status"))
            combined = round((0.65 * base) + (0.2 * recency) + (0.15 * success), 4)
            enriched = dict(incident)
            enriched["rerank_score"] = combined
            ranked.append((combined, enriched))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [item for _, item in ranked]

    @staticmethod
    def _recency_score(*raw_values: object) -> float:
        candidates = [value for value in raw_values if value]
        parsed_dates = []
        for value in candidates:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M", "%m/%d/%Y %H:%M", "%d/%m/%Y %H:%M"):
                try:
                    parsed_dates.append(datetime.strptime(str(value), fmt))
                    break
                except ValueError:
                    continue
        if not parsed_dates:
            return 0.2
        latest = max(parsed_dates)
        age_days = max((datetime.now() - latest).days, 0)
        return max(0.1, 1 / (1 + (age_days / 365)))

    @staticmethod
    def _resolution_success_score(status: object) -> float:
        code = str(status or "").lower()
        if code in {"resolved", "closed"}:
            return 0.85
        if code in {"in progress", "assigned"}:
            return 0.45
        if code in {"cancelled", "rejected"}:
            return 0.2
        if not code:
            return 0.3
        return 0.5
