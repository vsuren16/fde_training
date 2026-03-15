from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=500)
    category: str | None = None
    max_price: float | None = Field(default=None, gt=0)


class RecommendationItem(BaseModel):
    id: str
    name: str
    product_name: str | None = None
    category: str
    price: float
    image_url: str
    image_urls: list[str] = Field(default_factory=list)
    short_description: str | None = None
    description: str | None = None
    brand: str | None = None
    color: str | None = None
    size: str | None = None
    available: bool | None = None
    similarity_score: float


class RecommendResponse(BaseModel):
    query: str
    model_version: str
    latency_ms: float
    assistant_response: str
    results: list[RecommendationItem]
