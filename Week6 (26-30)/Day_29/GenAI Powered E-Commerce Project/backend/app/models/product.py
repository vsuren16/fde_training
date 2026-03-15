from pydantic import BaseModel, Field
from typing import Optional, List

class Product(BaseModel):
    id: str = Field(..., description="Product ID (stringified ObjectId or external id)")
    title: str
    description: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    tags: List[str] = []