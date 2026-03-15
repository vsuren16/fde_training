from pydantic import BaseModel, validator

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    total_copies: int

    @validator('isbn')
    def isbn_digits_only(cls, v):
        if not v.isdigit():
            raise ValueError('ISBN must be digits only')
        return v

    @validator('total_copies')
    def total_copies_positive(cls, v):
        if v <= 0:
            raise ValueError('total_copies must be greater than 0')
        return v

class BookResponse(BaseModel):
    _id: str
    title: str
    author: str
    isbn: str
    total_copies: int
    available_copies: int
    current_status: str
    last_transaction_id: str = None

class CheckoutRequest(BaseModel):
    borrower_name: str
    borrower_id: str
    due_days: int

    @validator('due_days')
    def due_days_range(cls, v):
        if not (1 <= v <= 30):
            raise ValueError('due_days must be between 1 and 30')
        return v

class ReturnRequest(BaseModel):
    borrower_id: str

class BookUpdate(BaseModel):
    title: str = None
    author: str = None
    isbn: str = None
    total_copies: int = None
    available_copies: int = None
    current_status: str = None
    last_transaction_id: str = None
