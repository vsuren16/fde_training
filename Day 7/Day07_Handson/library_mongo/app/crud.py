from datetime import datetime, timedelta
from pymongo import MongoClient
from bson import ObjectId


# Database connection
client = MongoClient("mongodb://localhost:27017")
db = client.library_db
books_col = db.books
transactions_col = db.transactions


def get_current_time():
    return datetime.utcnow()


def to_object_id(id_str: str, field_name: str = "id") -> ObjectId:
    """Safely convert string to ObjectId with a clean error."""
    try:
        return ObjectId(id_str)
    except Exception:
        raise ValueError(f"Invalid {field_name}")


def serialize_doc(doc: dict | None) -> dict | None:
    """Convert Mongo types to JSON-safe types."""
    if not doc:
        return doc

    for k, v in list(doc.items()):
        if isinstance(v, ObjectId):
            doc[k] = str(v)
        # datetime is usually OK in FastAPI, but converting keeps it consistent everywhere
        elif isinstance(v, datetime):
            doc[k] = v.isoformat()

    return doc


def serialize_docs(docs: list[dict]) -> list[dict]:
    return [serialize_doc(d) for d in docs]


def calculate_fine(return_date: datetime, due_date: datetime) -> float:
    """10 rs/day after due_date."""
    if not return_date or not due_date:
        return 0.0
    if return_date <= due_date:
        return 0.0
    days_late = (return_date - due_date).days
    return float(max(0, days_late * 10))


# -------------------------
# Books CRUD
# -------------------------
def create_book(payload: dict) -> dict:
    if books_col.find_one({"isbn": payload["isbn"]}):
        raise ValueError("ISBN already exists")

    payload["available_copies"] = payload["total_copies"]
    payload["current_status"] = "available"
    payload["last_transaction_id"] = None

    result = books_col.insert_one(payload)
    doc = {"_id": result.inserted_id, **payload}
    return serialize_doc(doc)


def list_books(status: str = None, author: str = None) -> list:
    query = {}
    if status:
        query["current_status"] = status
    if author:
        query["author"] = {"$regex": author, "$options": "i"}

    books = list(books_col.find(query))
    return serialize_docs(books)


def get_book(book_id: str) -> dict | None:
    oid = to_object_id(book_id, "book_id")
    book = books_col.find_one({"_id": oid})
    return serialize_doc(book)


def update_book(book_id: str, payload: dict) -> dict | None:
    oid = to_object_id(book_id, "book_id")
    result = books_col.update_one({"_id": oid}, {"$set": payload})
    if result.matched_count == 0:
        return None
    return get_book(book_id)


# -------------------------
# Transactions CRUD helpers
# -------------------------
def create_transaction(payload: dict) -> dict:
    result = transactions_col.insert_one(payload)
    doc = {"_id": result.inserted_id, **payload}
    return serialize_doc(doc)


def update_transaction(transaction_id: str, payload: dict) -> dict | None:
    oid = to_object_id(transaction_id, "transaction_id")
    result = transactions_col.update_one({"_id": oid}, {"$set": payload})
    if result.matched_count == 0:
        return None
    tx = transactions_col.find_one({"_id": oid})
    return serialize_doc(tx)


# -------------------------
# Business Logic
# -------------------------
def checkout_book(book_id: str, borrower_name: str, borrower_id: str, due_days: int = 7) -> dict:
    book_oid = to_object_id(book_id, "book_id")

    # 1) Find book available
    book = books_col.find_one({"_id": book_oid, "available_copies": {"$gt": 0}})
    if not book:
        raise ValueError("Book not found or not available")

    now = get_current_time()
    due_date = now + timedelta(days=due_days)

    transaction_payload = {
        "book_id": book_oid,
        "borrower_name": borrower_name,
        "borrower_id": borrower_id,
        "checkout_date": now,
        "due_date": due_date,
        "return_date": None,
        "status": "checked_out",
        "fine_amount": 0.0,
    }

    tx_result = transactions_col.insert_one(transaction_payload)
    tx_id = tx_result.inserted_id

    # 2) Update book atomically
    update_result = books_col.update_one(
        {"_id": book_oid, "available_copies": {"$gt": 0}},
        {
            "$inc": {"available_copies": -1},
            "$set": {"current_status": "checked_out", "last_transaction_id": tx_id},
        },
    )

    if update_result.matched_count == 0:
        transactions_col.delete_one({"_id": tx_id})
        raise ValueError("Failed to update book availability")

    doc = {"_id": tx_id, **transaction_payload}
    return serialize_doc(doc)


def return_book(book_id: str, borrower_id: str) -> dict:
    book_oid = to_object_id(book_id, "book_id")

    tx = transactions_col.find_one(
        {"book_id": book_oid, "borrower_id": borrower_id, "status": "checked_out"},
        sort=[("checkout_date", -1)],
    )
    if not tx:
        raise ValueError("No active checkout found for this book and borrower")

    now = get_current_time()
    fine = calculate_fine(now, tx["due_date"])

    update_tx_result = transactions_col.update_one(
        {"_id": tx["_id"]},
        {"$set": {"status": "returned", "return_date": now, "fine_amount": fine}},
    )
    if update_tx_result.matched_count == 0:
        raise ValueError("Failed to update transaction")

    update_book_result = books_col.update_one(
        {"_id": book_oid},
        {
            "$inc": {"available_copies": 1},
            "$set": {"current_status": "available", "last_transaction_id": tx["_id"]},
        },
    )
    if update_book_result.matched_count == 0:
        raise ValueError("Failed to update book")

    tx["status"] = "returned"
    tx["return_date"] = now
    tx["fine_amount"] = fine
    return serialize_doc(tx)


def list_transactions(book_id: str = None, status: str = None, borrower_id: str = None) -> list:
    query = {}

    if book_id:
        query["book_id"] = to_object_id(book_id, "book_id")
    if borrower_id:
        query["borrower_id"] = borrower_id

    if status == "overdue":
        query["status"] = "checked_out"
        query["due_date"] = {"$lt": get_current_time()}
    elif status:
        query["status"] = status

    txs = list(transactions_col.find(query))
    return serialize_docs(txs)
