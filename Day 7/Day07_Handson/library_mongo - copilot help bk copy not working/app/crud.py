from datetime import datetime, timedelta
from pymongo import MongoClient
from bson import ObjectId

# Database connection
client = MongoClient("mongodb://localhost:27017")
db = client.library_db
books_col = db.books
transactions_col = db.transactions

# Helper: Get current UTC time for overdue checks
def get_current_time():
    """Returns datetime.utcnow() for consistent date
    comparisons."""
    return datetime.utcnow()

# Usage in queries (copy-paste these examples)
def is_overdue(transaction):
    """Simple function to check if a transaction is overdue."""
    return transaction.get('status') == 'checked_out' and \
transaction.get('due_date') and \
transaction['due_date'] < get_current_time()

# Example in list_transactions (add this logic)
def list_overdue_transactions():
    now = get_current_time()
    overdue = list(transactions_col.find({
        "status": "checked_out",
        "due_date": {"$lt": now}  # Mongo filter equivalent of due_date < now
    }).sort("due_date"))
    return [{"title": books_col.find_one({"_id": t["book_id"]})["title"], **t} for t in overdue]  # Denormalize title for display
    
# Calculate fine (days late)
def calculate_fine(return_date, due_date):
    if not return_date or return_date > due_date:
        days_late = (get_current_time() - due_date).days
        return max(0, days_late * 10) # 10rs/day
    return 0.0

# CRUD functions for books
def create_book(payload: dict) -> dict:
    # Check if ISBN is unique
    if books_col.find_one({"isbn": payload["isbn"]}):
        raise ValueError("ISBN already exists")
    # Add default fields
    payload["available_copies"] = payload["total_copies"]
    payload["current_status"] = "available"
    payload["last_transaction_id"] = None
    result = books_col.insert_one(payload)
    return {"_id": str(result.inserted_id), **payload}

def list_books(status: str = None, author: str = None) -> list:
    query = {}
    if status:
        query["current_status"] = status
    if author:
        query["author"] = {"$regex": author, "$options": "i"}
    books = list(books_col.find(query))
    for book in books:
        book["_id"] = str(book["_id"])
    return books

def get_book(book_id: str) -> dict:
    book = books_col.find_one({"_id": ObjectId(book_id)})
    if book:
        book["_id"] = str(book["_id"])
    return book

def update_book(book_id: str, payload: dict) -> dict:
    result = books_col.update_one({"_id": ObjectId(book_id)}, {"$set": payload})
    if result.matched_count == 0:
        return None
    return get_book(book_id)

# CRUD functions for transactions
def create_transaction(payload: dict) -> dict:
    result = transactions_col.insert_one(payload)
    return {"_id": str(result.inserted_id), **payload}

def update_transaction(transaction_id: str, payload: dict) -> dict:
    result = transactions_col.update_one({"_id": ObjectId(transaction_id)}, {"$set": payload})
    if result.matched_count == 0:
        return None
    transaction = transactions_col.find_one({"_id": ObjectId(transaction_id)})
    if transaction:
        transaction["_id"] = str(transaction["_id"])
    return transaction

# Transaction logic functions
def checkout_book(book_id: str, borrower_name: str, borrower_id: str, due_days: int = 7) -> dict:
    # 1. Find book with available copies
    book = books_col.find_one({"_id": ObjectId(book_id), "available_copies": {"$gt": 0}})
    if not book:
        raise ValueError("Book not found or not available")
    
    # 2. Atomic update book
    now = get_current_time()
    due_date = now + timedelta(days=due_days)
    transaction_payload = {
        "book_id": ObjectId(book_id),
        "borrower_name": borrower_name,
        "borrower_id": borrower_id,
        "checkout_date": now,
        "due_date": due_date,
        "return_date": None,
        "status": "checked_out",
        "fine_amount": 0.0
    }
    tx_result = transactions_col.insert_one(transaction_payload)
    tx_id = tx_result.inserted_id
    
    # Update book atomically
    update_result = books_col.update_one(
        {"_id": ObjectId(book_id), "available_copies": {"$gt": 0}},
        {"$inc": {"available_copies": -1}, "$set": {"current_status": "checked_out", "last_transaction_id": tx_id}}
    )
    if update_result.matched_count == 0:
        # Rollback transaction insert
        transactions_col.delete_one({"_id": tx_id})
        raise ValueError("Failed to update book availability")
    
    return {"_id": str(tx_id), **transaction_payload}

def return_book(book_id: str, borrower_id: str) -> dict:
    # 1. Find last checked out transaction
    tx = transactions_col.find_one(
        {"book_id": ObjectId(book_id), "borrower_id": borrower_id, "status": "checked_out"},
        sort=[("checkout_date", -1)]
    )
    if not tx:
        raise ValueError("No active checkout found for this book and borrower")
    
    # 2. Calculate fine
    now = get_current_time()
    fine = calculate_fine(now, tx["due_date"])
    
    # 3. Update transaction
    update_tx_result = transactions_col.update_one(
        {"_id": tx["_id"]},
        {"$set": {"status": "returned", "return_date": now, "fine_amount": fine}}
    )
    if update_tx_result.matched_count == 0:
        raise ValueError("Failed to update transaction")
    
    # 4. Update book
    update_book_result = books_col.update_one(
        {"_id": ObjectId(book_id)},
        {"$inc": {"available_copies": 1}, "$set": {"current_status": "available"}}
    )
    if update_book_result.matched_count == 0:
        raise ValueError("Failed to update book")
    
    # Return updated transaction
    tx["status"] = "returned"
    tx["return_date"] = now
    tx["fine_amount"] = fine
    tx["_id"] = str(tx["_id"])
    return tx

def list_transactions(book_id: str = None, status: str = None, borrower_id: str = None) -> list:
    query = {}
    if book_id:
        query["book_id"] = ObjectId(book_id)
    if borrower_id:
        query["borrower_id"] = borrower_id
    if status == "overdue":
        query["status"] = "checked_out"
        query["due_date"] = {"$lt": get_current_time()}
    elif status:
        query["status"] = status
    
    transactions = list(transactions_col.find(query))
    for tx in transactions:
        tx["_id"] = str(tx["_id"])
        tx["book_id"] = str(tx["book_id"])
    return transactions