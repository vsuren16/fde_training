from typing import Optional
from pydantic import BaseModel, Field, validator
import re


class AccountCreate(BaseModel):
    account_holder: str = Field(..., min_length=3)
    account_number: str
    account_type: str
    total_balance: int = Field(..., gt=0)

    @validator("account_number")
    def validate_account_number(cls, v: str) -> str:
        if not re.match(r"^ACC\d{4,}$", v):
            raise ValueError("account_number must be in format ACCxxxx (digits)")
        return v

    @validator("account_type")
    def validate_account_type(cls, v: str) -> str:
        allowed = {"savings", "current"}
        if v not in allowed:
            raise ValueError(f"account_type must be one of {sorted(allowed)}")
        return v


class AccountResponse(BaseModel):
    _id: str
    account_holder: str
    account_number: str
    account_type: str

    total_balance: int
    current_balance: int
    account_status: str  
    last_transaction_id: Optional[str] = None

    @validator("account_status")
    def validate_account_status(cls, v: str) -> str:
        allowed = {"active", "inactive"}
        if v not in allowed:
            raise ValueError(f"account_status must be one of {sorted(allowed)}")
        return v

    @validator("current_balance")
    def validate_current_balance(cls, v: int) -> int:
        if v < 0:
            raise ValueError("current_balance cannot be negative")
        return v


class TransactionRequest(BaseModel):
    transaction_type: str
    amount: int = Field(..., gt=0)

    @validator("transaction_type")
    def validate_transaction_type(cls, v: str) -> str:
        allowed = {"credit", "debit"}
        if v not in allowed:
            raise ValueError(f"transaction_type must be one of {sorted(allowed)}")
        return v
