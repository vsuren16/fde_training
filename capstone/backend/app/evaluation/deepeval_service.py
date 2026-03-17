from __future__ import annotations

from app.schemas.incident import EvaluationResponse


class DeepEvalService:
    def run(self) -> EvaluationResponse:
        try:
            import deepeval  # noqa: F401

            return EvaluationResponse(
                framework="DeepEval",
                status="available",
                summary="DeepEval package is installed and ready for benchmark harness integration.",
                metrics={},
            )
        except Exception:
            return EvaluationResponse(
                framework="DeepEval",
                status="not_installed",
                summary=(
                    "DeepEval hooks are scaffolded, but the package is not installed in the "
                    "current environment yet."
                ),
                metrics={},
            )
