from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ProductSnippet(BaseModel):
    id: str
    title: str
    price: Optional[float] = None
    rating: Optional[float] = None
    review_summary: Optional[str] = None

class InsightsRequest(BaseModel):
    query: str = Field(..., min_length=3)
    products: List[ProductSnippet] = Field(default_factory=list)
    max_items: int = Field(5, ge=1, le=10)

class InsightItem(BaseModel):
    product_id: str
    title: str
    best_for: List[str] = Field(default_factory=list)
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"] = "medium"

class InsightsResponse(BaseModel):
    answer: str
    items: List[InsightItem] = Field(default_factory=list)
    safety_notes: List[str] = Field(default_factory=list)