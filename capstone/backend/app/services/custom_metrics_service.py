from __future__ import annotations

from statistics import median


class CustomMetricsService:
    def predict_resolution_time_hours(self, incidents: list[dict]) -> float | None:
        hours = [
            float(item["resolution_time_hours"])
            for item in incidents
            if item.get("resolution_time_hours") not in {None, "", "nan"}
            and 0 < float(item["resolution_time_hours"]) <= 720
        ]
        if not hours:
            return None
        return round(float(median(hours)), 2)

    def predict_fix_accuracy(self, incidents: list[dict], judge_score: float | None) -> float | None:
        if not incidents:
            return None
        resolution_quality = sum(
            1.0
            for item in incidents
            if str(item.get("status", "")).lower() in {"resolved", "closed"}
        ) / len(incidents)
        groundedness = judge_score if judge_score is not None else 0.4
        return round((0.55 * resolution_quality) + (0.45 * groundedness), 4)
