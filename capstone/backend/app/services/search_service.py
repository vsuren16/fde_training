from __future__ import annotations
from time import perf_counter

from app.core.container import get_incident_repository, get_openai_adapter, get_vector_store
from app.evaluation.judge_service import JudgeService, JudgeVerdict
from app.guardrails.output_guardrails import validate_grounded_response
from app.observability.langsmith import traced
from app.schemas.incident import IncidentResult, SearchRequest, SearchResponse
from app.services.a2a_service import A2AService
from app.services.agent_handoff_service import AgentHandoffService
from app.services.custom_metrics_service import CustomMetricsService
from app.services.keyword_search_service import KeywordSearchService, tokenize
from app.services.reranking_service import RerankingService
from app.services.resolution_service import ResolutionService
from app.services.root_cause_service import RootCauseService
from app.services.routing_service import RoutingService
from app.services.search_diagnostics_service import SearchDiagnosticsSnapshot
from app.services.token_optimization_service import TokenOptimizationService
from app.services.troubleshooting_validator_service import TroubleshootingValidatorService
from app.services.triage_service import TriageService

LOW_SIGNAL_QUERY_TOKENS = {
    "user",
    "users",
    "employee",
    "employees",
    "issue",
    "problem",
    "incident",
    "system",
    "application",
    "app",
    "device",
    "machine",
    "computer",
    "laptop",
    "desktop",
}

INTENT_GROUPS = {
    "auth": {"password", "credential", "credentials", "login", "signin", "sign", "account", "locked", "unlock", "expired", "mfa", "authentication"},
    "network": {"network", "vpn", "proxy", "citrix", "dns", "latency", "connectivity", "remote"},
    "database": {"database", "query", "sql", "postgresql", "connection", "pool", "timeout"},
    "hardware": {"boot", "bios", "device", "ssd", "reboot", "startup", "battery", "screen"},
}


class SearchService:
    def __init__(self, keyword_search_service: KeywordSearchService) -> None:
        self.keyword_search_service = keyword_search_service
        self.repository = get_incident_repository()
        self.openai = get_openai_adapter()
        self.vector_store = get_vector_store()
        self.triage_service = TriageService()
        self.routing_service = RoutingService()
        self.resolution_service = ResolutionService(self.openai)
        self.judge_service = JudgeService(self.openai)
        self.reranking_service = RerankingService()
        self.metrics_service = CustomMetricsService()
        self.troubleshooting_validator = TroubleshootingValidatorService()
        self.token_optimizer = TokenOptimizationService()
        self.agent_handoff_service = AgentHandoffService()
        self.a2a_service = A2AService()
        self.root_cause_service = RootCauseService(self.openai)

    def warm(self) -> int:
        incidents = self.repository.fetch_all()
        self.keyword_search_service.load(incidents)
        return len(incidents)

    @traced(run_type="chain", name="incident_search")
    def search(self, payload: SearchRequest) -> SearchResponse:
        started_at = perf_counter()
        filters = payload.filters.model_dump(exclude_none=True) if payload.filters else None
        keyword_hits = self.keyword_search_service.search(payload.query, payload.top_k * 2, filters)
        semantic_hits = self._semantic_search(payload.query, payload.top_k * 2, filters)
        merged = self._merge_hits(keyword_hits, semantic_hits)
        incident_ids = [item["incident_id"] for item in merged[: payload.top_k]]
        incidents = self.repository.fetch_by_ids(incident_ids)
        score_lookup = {item["incident_id"]: item["score"] for item in merged}
        incidents = self.reranking_service.rerank(incidents, score_lookup)

        triage_priority = self.triage_service.classify_priority(payload.query, incidents)
        response_mode = "grounded"
        response_notice = None

        if not self._has_relevant_internal_evidence(payload.query, incidents, score_lookup):
            incidents = []
            resolution_summary, llm_routed = self.resolution_service.best_effort_guidance(payload.query)
            degraded = True
            response_mode = "llm_fallback"
            response_notice = (
                "We did not find sufficiently relevant incident evidence in the internal knowledge base "
                "for this query, so the request was routed to an AI model for best-effort guidance."
                if llm_routed
                else "We did not find sufficiently relevant incident evidence in the internal knowledge base, "
                "and the LLM fallback path was unavailable. Refine the query or escalate for manual triage."
            )
            verdict = JudgeVerdict(
                status="degraded",
                score=0.0,
                reason=(
                    "Internal evidence was not sufficiently relevant to ground a knowledge-base answer. "
                    "A disclosed LLM fallback response was used instead."
                ),
                approved=False,
            )
        else:
            evidence = self.token_optimizer.select_evidence(incidents)
            resolution_summary, degraded = self.resolution_service.summarize(payload.query, evidence)
            verdict = self.judge_service.evaluate(
                payload.query,
                evidence,
                resolution_summary,
                use_llm=not degraded,
            )

            if not verdict.approved:
                resolution_summary = self._safe_grounded_fallback(payload.query, incidents)
                degraded = True
                response_mode = "grounded_fallback"
                response_notice = (
                    "The retrieved incidents were only partially grounded for this query, "
                    "so the answer was downgraded to a conservative evidence-backed fallback."
                )

        handoff_path = self.agent_handoff_service.handoff_path(triage_priority, incidents)
        route_to = handoff_path[-1] if handoff_path else self.routing_service.route(incidents)
        troubleshooting_validation = self.troubleshooting_validator.validate(
            verdict.status,
            verdict.score,
            verdict.reason,
        )
        agent_messages = self.a2a_service.build_messages(handoff_path, payload.query, incidents)
        root_cause_summary = self.root_cause_service.summarize(payload.query, incidents, handoff_path)
        predicted_resolution_time_hours = self.metrics_service.predict_resolution_time_hours(incidents)
        predicted_fix_accuracy = self.metrics_service.predict_fix_accuracy(incidents, verdict.score)

        response = SearchResponse(
            query=payload.query,
            triage_priority=triage_priority,
            route_to=route_to,
            handoff_path=handoff_path,
            resolution_summary=resolution_summary,
            response_mode=response_mode,
            response_notice=response_notice,
            root_cause_summary=root_cause_summary,
            predicted_resolution_time_hours=predicted_resolution_time_hours,
            predicted_fix_accuracy=predicted_fix_accuracy,
            troubleshooting_validation=troubleshooting_validation,
            agent_messages=agent_messages,
            incidents=[
                IncidentResult(
                    incident_id=item["incident_id"],
                    title=item.get("title", "Untitled incident"),
                    category=item.get("category"),
                    priority=self._safe_int(item.get("priority")),
                    priority_label=item.get("priority_label"),
                    status=item.get("status"),
                    team=item.get("team"),
                    assigned_to=item.get("assigned_to"),
                    similarity_score=round(score_lookup.get(item["incident_id"], 0.0), 4),
                    rerank_score=item.get("rerank_score"),
                    description=item.get("description", ""),
                    incident_text=item.get("incident_text", ""),
                    resolution_notes=item.get("resolution_notes"),
                )
                for item in incidents
            ],
            degraded=degraded,
            judge_status=verdict.status,
            judge_score=verdict.score,
            judge_reason=verdict.reason,
        )
        diagnostics = SearchDiagnosticsSnapshot(
            query=payload.query,
            duration_ms=int((perf_counter() - started_at) * 1000),
            degraded=degraded,
            judge_status=verdict.status,
            judge_score=verdict.score,
            route_to=route_to,
            handoff_path=handoff_path,
            incidents_retrieved=len(incidents),
            trace_url=self.openai.settings.langsmith_project_url or None,
        )
        from app.services.runtime_state import get_search_diagnostics_service

        get_search_diagnostics_service().record(diagnostics)
        return validate_grounded_response(response)

    def _semantic_search(self, query: str, top_k: int, filters: dict | None) -> list[dict]:
        if not self.openai.enabled:
            return []
        try:
            query_embedding = self.openai.embed_texts([query])[0]
            where = {
                key: value
                for key, value in (filters or {}).items()
                if key in {"priority", "category", "status", "team"}
            } or None
            hits = self.vector_store.query(query_embedding, top_k, where=where)
            return [
                {
                    "incident_id": item["incident_id"],
                    "score": 1.0 / (1.0 + item["distance"]),
                }
                for item in hits
            ]
        except Exception:
            return []

    @staticmethod
    def _merge_hits(keyword_hits: list[dict], semantic_hits: list[dict]) -> list[dict]:
        merged: dict[str, float] = {}
        for hit in keyword_hits:
            merged[hit["incident_id"]] = merged.get(hit["incident_id"], 0.0) + (0.45 * hit["score"])
        for hit in semantic_hits:
            merged[hit["incident_id"]] = merged.get(hit["incident_id"], 0.0) + (0.55 * hit["score"])
        return [
            {"incident_id": incident_id, "score": score}
            for incident_id, score in sorted(merged.items(), key=lambda entry: entry[1], reverse=True)
        ]

    @staticmethod
    def _safe_int(value: object) -> int | None:
        if value is None:
            return None
        try:
            if str(value) == "nan":
                return None
            return int(float(value))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _has_relevant_internal_evidence(
        query: str,
        incidents: list[dict],
        score_lookup: dict[str, float],
    ) -> bool:
        if not incidents:
            return False

        query_tokens = set(tokenize(query))
        if not query_tokens:
            return False

        top_incidents = incidents[:3]
        evidence_tokens: set[str] = set()
        for incident in top_incidents:
            evidence_tokens.update(tokenize(str(incident.get("title") or "")))
            evidence_tokens.update(tokenize(str(incident.get("description") or "")))
            evidence_tokens.update(tokenize(str(incident.get("incident_text") or "")))
            evidence_tokens.update(tokenize(str(incident.get("resolution_notes") or "")))
            evidence_tokens.update(tokenize(str(incident.get("category") or "")))
            evidence_tokens.update(tokenize(str(incident.get("team") or "")))

        overlap_ratio = len(query_tokens & evidence_tokens) / max(len(query_tokens), 1)
        significant_query_tokens = {token for token in query_tokens if token not in LOW_SIGNAL_QUERY_TOKENS}
        significant_overlap_ratio = (
            len(significant_query_tokens & evidence_tokens) / max(len(significant_query_tokens), 1)
            if significant_query_tokens
            else overlap_ratio
        )
        max_score = max(score_lookup.get(item["incident_id"], 0.0) for item in top_incidents)
        has_resolution_notes = any(str(item.get("resolution_notes") or "").strip() for item in top_incidents)
        if not SearchService._intent_groups_match(query_tokens, evidence_tokens):
            return False
        return (
            overlap_ratio >= 0.18
            and significant_overlap_ratio >= 0.34
            and max_score >= 0.15
            and has_resolution_notes
        )

    @staticmethod
    def _intent_groups_match(query_tokens: set[str], evidence_tokens: set[str]) -> bool:
        for group_tokens in INTENT_GROUPS.values():
            query_has_group = bool(query_tokens & group_tokens)
            if query_has_group and not (evidence_tokens & group_tokens):
                return False
        return True

    @staticmethod
    def _safe_grounded_fallback(query: str, incidents: list[dict]) -> str:
        if not incidents:
            return (
                "The system could not produce a grounded resolution summary for this query. "
                "Refine the query or broaden the search filters."
            )

        top = incidents[0]
        return (
            f"The generated answer was downgraded because grounding confidence was low for the query: {query}. "
            f"Start by reviewing incident {top.get('incident_id')} titled '{top.get('title', 'unknown')}' "
            f"in category {top.get('category', 'unknown')} handled by {top.get('team', 'the current team')}. "
            "Use the retrieved incidents and their resolution notes as evidence before applying "
            "any remediation."
        )
