from __future__ import annotations

from app.core.container import get_incident_repository
from app.schemas.incident import FeedbackRequest, FeedbackResponse


class FeedbackService:
    def __init__(self) -> None:
        self.repository = get_incident_repository()

    def store(self, payload: FeedbackRequest) -> FeedbackResponse:
        self.repository.store_feedback(payload.model_dump())
        return FeedbackResponse(status="accepted", stored=True)
