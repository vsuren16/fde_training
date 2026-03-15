from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

from .database import accounts_col, transactions_col

def to_object_id(id_str: str, field_name: str = "id") -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid {field_name}")


def serialize_doc(doc: dict | None) -> dict | None:
    """Convert Mongo types to JSON-safe values."""
    if not doc:
        return doc

    for k, v in list(doc.items()):
        if isinstance(v, ObjectId):
            doc[k] = str(v)
        elif isinstance(v, datetime):
            doc[k] = v.isoformat()
    return doc


def serialize_docs(docs: list[dict]) -> list[dict]:
    return [serialize_doc(d) for d in docs]


def status_from_balance(current_balance: int) -> str:
    return "active" if current_balance >= 0 else "inactive"


def create_account(payload: dict) -> dict:
    # Ensure unique account_number
    if accounts_col.find_one({"account_number": payload["account_number"]}):
        raise HTTPException(status_code=400, detail="account_number already exists")

    # Initialize denormalized/derived fields
    payload["current_balance"] = int(payload["total_balance"])
    payload["account_status"] = status_from_balance(payload["current_balance"])
    payload["last_transaction_id"] = None

    res = accounts_col.insert_one(payload)
    doc = {"_id": res.inserted_id, **payload}
    return serialize_doc(doc)


def list_accounts(status: str = None, account_type: str = None) -> list:
    query: dict = {}
    if status:
        query["account_status"] = status
    if account_type:
        query["account_type"] = account_type

    accounts = list(accounts_col.find(query))
    return serialize_docs(accounts)


def get_account(account_id: str) -> dict:
    oid = to_object_id(account_id, "account_id")
    acc = accounts_col.find_one({"_id": oid})
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return serialize_doc(acc)


def update_account(account_id: str, payload: dict) -> dict:
    oid = to_object_id(account_id, "account_id")

    if "account_number" in payload:
        existing = accounts_col.find_one(
            {"account_number": payload["account_number"], "_id": {"$ne": oid}}
        )
        if existing:
            raise HTTPException(status_code=400, detail="account_number already exists")

    res = accounts_col.update_one({"_id": oid}, {"$set": payload})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Account not found")

    if "current_balance" in payload:
        accounts_col.update_one(
            {"_id": oid},
            {"$set": {"account_status": status_from_balance(int(payload["current_balance"]))}},
        )

    updated = accounts_col.find_one({"_id": oid})
    return serialize_doc(updated)



def perform_transaction(account_id: str, req) -> dict:
    """
    req is expected to have:
      - req.transaction_type in {"credit","debit"}
      - req.amount > 0
    (Validated at API layer via Pydantic)
    """
    oid = to_object_id(account_id, "account_id")

    # 1) Find account
    account = accounts_col.find_one({"_id": oid})
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    amount = int(req.amount)
    ttype = req.transaction_type
    current_balance = int(account.get("current_balance", 0))

    # 2) Validate balance for debit (no overdraft allowed)
    if ttype == "debit" and amount > current_balance:
        raise HTTPException(status_code=400, detail="Insufficient balance for debit")

    inc = amount if ttype == "credit" else -amount

    update_res = accounts_col.find_one_and_update(
        {"_id": oid},
        {"$inc": {"current_balance": inc}},
        return_document=True,  
    )

    if not update_res:
        raise HTTPException(status_code=404, detail="Account not found")

    new_balance = int(update_res["current_balance"])
    acc_status = status_from_balance(new_balance)

    accounts_col.update_one({"_id": oid}, {"$set": {"account_status": acc_status}})

    tx_payload = {
        "account_id": oid,
        "account_holder": update_res.get("account_holder"),  # denormalized
        "transaction_type": ttype,  # credit/debit
        "amount": amount,
        "transaction_date": datetime.utcnow(),
        "status": "completed",
        "balance_after_transaction": new_balance,
    }

    tx_res = transactions_col.insert_one(tx_payload)
    tx_id = tx_res.inserted_id

    accounts_col.update_one({"_id": oid}, {"$set": {"last_transaction_id": tx_id}})

    tx_doc = {"_id": tx_id, **tx_payload}
    return serialize_doc(tx_doc)


def list_transactions(account_id: str = None, transaction_type: str = None) -> list:
    query: dict = {}
    if account_id:
        query["account_id"] = to_object_id(account_id, "account_id")
    if transaction_type:
        query["transaction_type"] = transaction_type

    txs = list(transactions_col.find(query).sort("transaction_date", -1))
    return serialize_docs(txs)
