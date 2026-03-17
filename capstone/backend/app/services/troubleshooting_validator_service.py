from __future__ import annotations

from app.schemas.incident import TroubleshootingValidation


class TroubleshootingValidatorService:
    def validate(self, status: str, score: float, reason: str) -> TroubleshootingValidation:
        return TroubleshootingValidation(
            status=status,
            score=score,
            reason=reason,
        )
