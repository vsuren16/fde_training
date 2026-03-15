"""Future-ready AI resiliency primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass
class CircuitBreaker:
    failure_threshold: int = 3
    failures: int = 0
    open: bool = False

    def call(self, primary: Callable[[], T], fallback: Callable[[], T]) -> T:
        if self.open:
            return fallback()
        try:
            result = primary()
            self.failures = 0
            return result
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.open = True
            return fallback()
