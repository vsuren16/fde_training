# app/schemas.py - basic models
from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional, List
from fastapi import APIRouter

router = APIRouter(prefix='/schemas', tags = ['schema'])

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example='T-shirt') # ... means: this field is REQUIRED.
    description: Optional[str] = Field(None, example='100% cotton')

class ItemCreate(ItemBase):
    price: float = Field(..., gt=0, example=199.99)

class ItemRead(ItemBase):
    model_config = ItemBase.model_config | ConfigDict(from_attributes=True) # allow from_orm conversions
    id: int
    price: float
