from app.services.agent_handoff_service import AgentHandoffService
from app.services.reranking_service import RerankingService


def test_handoff_service_escalates_network_priority_two() -> None:
    service = AgentHandoffService()
    path = service.handoff_path(
        2,
        [{"category": "Network"}],
    )
    assert path == ["L1_SUPPORT", "L2_INFRA", "L3_NETWORK_SPECIALIST"]


def test_reranker_adds_rerank_score() -> None:
    service = RerankingService()
    incidents = service.rerank(
        [
            {
                "incident_id": "INC-1",
                "status": "Resolved",
                "updated_at": "2025-12-03 10:00:00",
                "closed_at": "2025-12-03 11:00:00",
            }
        ],
        {"INC-1": 0.8},
    )

    assert incidents[0]["rerank_score"] is not None
