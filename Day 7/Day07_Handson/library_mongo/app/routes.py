from fastapi import APIRouter, HTTPException
from .crud import (
    create_book, list_books, get_book, update_book,
    checkout_book, return_book, list_transactions
)
from .models import BookCreate, CheckoutRequest, ReturnRequest, BookUpdate

router = APIRouter(prefix="/library", tags=["library"])


@router.post("/books/")
async def create_book_endpoint(payload: BookCreate):
    try:
        return create_book(payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/books/")
async def list_books_endpoint(current_status: str = None, author: str = None):
    try:
        return list_books(current_status, author)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/books/{book_id}")
async def get_book_endpoint(book_id: str):
    try:
        book = get_book(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/books/{book_id}")
async def update_book_endpoint(book_id: str, payload: BookUpdate):
    try:
        update_data = payload.dict(exclude_unset=True)
        # optional extra: remove None values if client sends them explicitly
        update_data = {k: v for k, v in update_data.items() if v is not None}

        updated_book = update_book(book_id, update_data)
        if not updated_book:
            raise HTTPException(status_code=404, detail="Book not found")
        return updated_book
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transactions/checkout/{book_id}")
async def checkout_book_endpoint(book_id: str, req: CheckoutRequest):
    try:
        return checkout_book(book_id, req.borrower_name, req.borrower_id, req.due_days)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transactions/return/{book_id}")
async def return_book_endpoint(book_id: str, req: ReturnRequest):
    try:
        return return_book(book_id, req.borrower_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transactions/")
async def list_transactions_endpoint(book_id: str = None, tx_status: str = None, borrower_id: str = None):
    try:
        return list_transactions(book_id, tx_status, borrower_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
