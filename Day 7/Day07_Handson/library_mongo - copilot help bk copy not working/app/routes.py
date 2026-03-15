from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from bson import ObjectId
from .crud import (
    create_book, list_books, get_book, update_book,
    checkout_book, return_book, list_transactions
)
from .models import BookCreate, BookResponse, CheckoutRequest, ReturnRequest, BookUpdate

# Remove the model definitions here as they are now in models.py

router = APIRouter(prefix="/library", tags=["library"])

@router.post("/books/")
async def create_book_endpoint(payload: BookCreate):
    try:
        book = create_book(payload.dict())
        return book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/books/")
async def list_books_endpoint(status: str = None, author: str = None):
    try:
        books = list_books(status, author)
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/books/{book_id}")
async def get_book_endpoint(book_id: str):
    try:
        book = get_book(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/books/{book_id}")
async def update_book_endpoint(book_id: str, payload: BookUpdate):
    try:
        update_data = {k: v for k, v in payload.dict().items() if v is not None}
        updated_book = update_book(book_id, update_data)
        if not updated_book:
            raise HTTPException(status_code=404, detail="Book not found")
        return updated_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transactions/checkout/{book_id}")
async def checkout_book_endpoint(book_id: str, req: CheckoutRequest):
    try:
        transaction = checkout_book(book_id, req.borrower_name, req.borrower_id, req.due_days)
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/transactions/return/{book_id}")
async def return_book_endpoint(book_id: str, req: ReturnRequest):
    try:
        transaction = return_book(book_id, req.borrower_id)
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/transactions/")
async def list_transactions_endpoint(book_id: str = None, status: str = None, borrower_id: str = None):
    try:
        transactions = list_transactions(book_id, status, borrower_id)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))