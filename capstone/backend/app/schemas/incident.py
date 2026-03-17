from pydantic import BaseModel, Field, field_validator

from app.guardrails.input_guardrails import validate_query_text


class IncidentFilter(BaseModel):
    priority: int | None = Field(default=None, ge=1, le=5)
    category: str | None = Field(default=None, min_length=2, max_length=100)
    status: str | None = Field(default=None, min_length=2, max_length=100)
    team: str | None = Field(default=None, min_length=2, max_length=150)


class SearchRequest(BaseModel):
    query: str = Field(min_length=8, max_length=2000)
    filters: IncidentFilter | None = None
    top_k: int = Field(default=5, ge=1, le=20)

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:
        return validate_query_text(value)


class IncidentResult(BaseModel):
    incident_id: str
    title: str
    category: str | None = None
    priority: int | None = None
    priority_label: str | None = None
    status: str | None = None
    team: str | None = None
    assigned_to: str | None = None
    similarity_score: float | None = None
    rerank_score: float | None = None
    description: str
    incident_text: str
    resolution_notes: str | None = None


class TroubleshootingValidation(BaseModel):
    status: str
    score: float
    reason: str


class AgentMessage(BaseModel):
    from_agent: str
    to_agent: str
    message: str


class SearchResponse(BaseModel):
    query: str
    triage_priority: int | None = None
    route_to: str
    handoff_path: list[str] = []
    resolution_summary: str
    response_mode: str = "grounded"
    response_notice: str | None = None
    root_cause_summary: str | None = None
    predicted_resolution_time_hours: float | None = None
    predicted_fix_accuracy: float | None = None
    troubleshooting_validation: TroubleshootingValidation | None = None
    agent_messages: list[AgentMessage] = []
    incidents: list[IncidentResult]
    degraded: bool = False
    judge_status: str = "not_run"
    judge_score: float | None = None
    judge_reason: str | None = None


class IngestionPreviewResponse(BaseModel):
    source_rows: int
    cleaned_rows: int
    dropped_rows: int
    required_columns: list[str]
    retrieval_strategy: str
    resolution_strategy: str


class IngestionRunResponse(BaseModel):
    processed_dataset_path: str
    documents_in_mongo: int
    vectors_in_chroma: int
    records_upserted: int
    embeddings_indexed: int
    vector_mode: str


class IngestionStatusResponse(BaseModel):
    documents_in_mongo: int
    vectors_in_chroma: int
    keyword_index_loaded: bool


class MetadataOptionsResponse(BaseModel):
    categories: list[str]
    teams: list[str]


class FeedbackRequest(BaseModel):
    query: str = Field(min_length=8, max_length=2000)
    incident_id: str
    rating: int = Field(ge=1, le=5)
    feedback_text: str | None = Field(default=None, max_length=1000)
    accepted: bool


class FeedbackResponse(BaseModel):
    status: str
    stored: bool


class EvaluationResponse(BaseModel):
    framework: str
    status: str
    summary: str
    metrics: dict[str, float]
