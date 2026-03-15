from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class MetricsStore:
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.touch()

    def append(self, row: dict) -> None:
        row = dict(row)
        row.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    def read_all(self) -> list[dict]:
        out: list[dict] = []
        with self.log_file.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return out

    def summary(self) -> dict:
        rows = self.read_all()
        if not rows:
            return {
                "average_relevance": 0.0,
                "average_faithfulness": 0.0,
                "average_completeness": 0.0,
                "daily_trend": {},
                "total_queries_evaluated": 0,
            }

        def mean(key: str) -> float:
            vals = [float(r.get("evaluation_score", {}).get(key, 0)) for r in rows]
            return round(sum(vals) / max(len(vals), 1), 3)

        trend: dict[str, list[float]] = {}
        for r in rows:
            ts = str(r.get("timestamp", ""))
            day = ts[:10] if len(ts) >= 10 else "unknown"
            trend.setdefault(day, []).append(float(r.get("evaluation_score", {}).get("overall_score", 0)))

        daily_trend = {d: round(sum(v) / max(len(v), 1), 3) for d, v in trend.items()}
        return {
            "average_relevance": mean("relevance"),
            "average_faithfulness": mean("faithfulness"),
            "average_completeness": mean("completeness"),
            "daily_trend": daily_trend,
            "total_queries_evaluated": len(rows),
        }
