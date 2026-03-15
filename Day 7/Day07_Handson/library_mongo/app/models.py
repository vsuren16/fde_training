# app/models.py

from typing import Optional
from pydantic import BaseModel, Field, validator


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    isbn: str = Field(..., min_length=13)
    total_copies: int = Field(..., gt=0)

    @validator("isbn")
    def isbn_digits_only(cls, v: str) -> str:
        # requirement: digits only + min_len=13
        if not v.isdigit():
            raise ValueError("ISBN must be digits only")
        return v


class BookResponse(BaseModel):
    # Mongo returns _id; we store it as string in API responses
    _id: str

    title: str
    author: str
    isbn: str
    total_copies: int

    available_copies: int
    current_status: str  # "available", "checked_out", "maintenance"
    last_transaction_id: Optional[str] = None

    @validator("current_status")
    def validate_status(cls, v: str) -> str:
        allowed = {"available", "checked_out", "maintenance"}
        if v not in allowed:
            raise ValueError(f"current_status must be one of {sorted(allowed)}")
        return v

    @validator("available_copies")
    def available_copies_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("available_copies must be >= 0")
        return v


class CheckoutRequest(BaseModel):
    borrower_name: str = Field(..., min_length=1)
    borrower_id: str = Field(..., min_length=1)
    due_days: int = Field(..., ge=1, le=30)


class ReturnRequest(BaseModel):
    borrower_id: str = Field(..., min_length=1)


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    isbn: Optional[str] = Field(None, min_length=13)
    total_copies: Optional[int] = Field(None, gt=0)
    available_copies: Optional[int] = Field(None, ge=0)
    current_status: Optional[str] = None
    last_transaction_id: Optional[str] = None

    @validator("isbn")
    def isbn_digits_only_if_provided(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.isdigit():
            raise ValueError("ISBN must be digits only")
        return v

    @validator("current_status")
    def validate_status_if_provided(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed = {"available", "checked_out", "maintenance"}
        if v not in allowed:
            raise ValueError(f"current_status must be one of {sorted(allowed)}")
        return v
