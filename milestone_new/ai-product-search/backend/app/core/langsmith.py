from __future__ import annotations

import os
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any

from app.core.config import settings

try:
    from langsmith import tracing_context
    from langsmith.run_helpers import trace
except ImportError:  # pragma: no cover
    tracing_context = None
    trace = None


def configure_langsmith() -> None:
    if settings.openai_api_key:
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key
    if settings.langsmith_api_key:
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
    os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint
    tracing_value = "true" if settings.langsmith_tracing else "false"
    os.environ["LANGSMITH_TRACING"] = tracing_value
    os.environ["LANGCHAIN_TRACING_V2"] = tracing_value


def langsmith_enabled() -> bool:
    return bool(settings.langsmith_tracing and settings.langsmith_api_key and trace and tracing_context)


@dataclass
class NoopTrace:
    metadata: dict[str, Any] = field(default_factory=dict)

    def end(self, outputs: dict[str, Any] | None = None) -> None:
        return


@asynccontextmanager
async def trace_run(
    name: str,
    run_type: str = "chain",
    *,
    inputs: dict[str, Any] | None = None,
    tags: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
):
    if not langsmith_enabled():
        yield NoopTrace(metadata=metadata or {})
        return

    with tracing_context(
        project_name=settings.langsmith_project,
        enabled=True,
        tags=tags,
        metadata=metadata,
    ):
        with trace(
            name,
            run_type=run_type,
            inputs=inputs,
            project_name=settings.langsmith_project,
            tags=tags,
            metadata=metadata,
        ) as run:
            yield run
