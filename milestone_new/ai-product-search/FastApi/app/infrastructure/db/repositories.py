import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models import SearchHistory


class SearchHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_record(self, query_text: str, model_version: str, latency_ms: float, scores: list[float]) -> None:
        record = SearchHistory(
            query_text=query_text,
            model_version=model_version,
            latency_ms=latency_ms,
            top_scores=json.dumps(scores),
        )
        self.session.add(record)
        await self.session.commit()
