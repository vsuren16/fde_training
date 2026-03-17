from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from time import time
from typing import Any


@dataclass
class SearchDiagnosticsSnapshot:
    query: str
    duration_ms: int
    degraded: bool
    judge_status: str
    judge_score: float | None
    route_to: str | None
    handoff_path: list[str] = field(default_factory=list)
    incidents_retrieved: int = 0
    trace_url: str | None = None
    recorded_at_epoch: int = field(default_factory=lambda: int(time()))

    def as_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "duration_ms": self.duration_ms,
            "degraded": self.degraded,
            "judge_status": self.judge_status,
            "judge_score": self.judge_score,
            "route_to": self.route_to,
            "handoff_path": self.handoff_path,
            "incidents_retrieved": self.incidents_retrieved,
            "trace_url": self.trace_url,
            "recorded_at_epoch": self.recorded_at_epoch,
        }


class SearchDiagnosticsService:
    def __init__(self) -> None:
        self._lock = Lock()
        self._latest: SearchDiagnosticsSnapshot | None = None

    def record(self, snapshot: SearchDiagnosticsSnapshot) -> None:
        with self._lock:
            self._latest = snapshot

    def get_latest(self) -> dict[str, Any] | None:
        with self._lock:
            return self._latest.as_dict() if self._latest else None
