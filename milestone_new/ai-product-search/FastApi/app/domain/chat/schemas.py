from pydantic import BaseModel, Field


class ChatAskRequest(BaseModel):
    message: str = Field(min_length=2, max_length=1200)


class ChatSource(BaseModel):
    source_type: str
    source_id: str
    snippet: str


class ChatAskResponse(BaseModel):
    answer: str
    model_version: str
    latency_ms: float
    used_guardrail: bool
    sources: list[ChatSource] = Field(default_factory=list)
