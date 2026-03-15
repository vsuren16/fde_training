from fastapi import APIRouter, Body, HTTPException, Path, Query
from .crud import (
    create_account,
    list_accounts,
    get_account,
    update_account,
    perform_transaction,
    list_transactions,
)
from .models import AccountCreate, TransactionRequest

router = APIRouter(prefix="/bank", tags=["bank"])


@router.post("/accounts/{account_id}")
def create_account_endpoint(
    account_id: int = Path(..., gt=0, description="Account ID must be > 0 (API-level id)"),
    account_type: str = Query(..., description="Account type: savings/current"),
    payload: AccountCreate = Body(...),
):
    """
    Note:
    - Mongo will still create its own _id (ObjectId).
    - account_id here is just to satisfy the 'Path param' requirement from class style.
    - We store account_id as a field too for reference.
    """
    allowed = {"savings", "current"}
    if account_type not in allowed:
        raise HTTPException(status_code=422, detail="account_type must be savings or current")

    data = payload.dict()
    data["account_type"] = account_type
    data["account_id"] = account_id  # optional: keep the numeric id in doc

    return create_account(data)


@router.get("/accounts/")
def list_accounts_endpoint(
    status: str = Query(None, description="Filter by account_status: active/inactive"),
    account_type: str = Query(None, description="Filter by account_type: savings/current"),
):
    if status and status not in {"active", "inactive"}:
        raise HTTPException(status_code=422, detail="status must be active or inactive")
    if account_type and account_type not in {"savings", "current"}:
        raise HTTPException(status_code=422, detail="account_type must be savings or current")

    return list_accounts(status=status, account_type=account_type)


@router.get("/accounts/{account_oid}")
def get_account_endpoint(
    account_oid: str = Path(..., description="Mongo ObjectId of the account"),
):
    return get_account(account_oid)


@router.put("/accounts/{account_oid}")
def update_account_endpoint(
    account_oid: str = Path(..., description="Mongo ObjectId of the account"),
    payload: dict = Body(..., description="Provide fields to update"),
):
    return update_account(account_oid, payload)


@router.post("/transactions/{account_oid}")
def perform_transaction_endpoint(
    account_oid: str = Path(..., description="Mongo ObjectId of the account"),
    transaction_type: str = Query(..., description="credit/debit"),
    req: TransactionRequest = Body(...),
):
    """
    Uses:
    - Path: account_oid
    - Query: transaction_type
    - Body: amount (in TransactionRequest)
    """
    if transaction_type not in {"credit", "debit"}:
        raise HTTPException(status_code=422, detail="transaction_type must be credit or debit")

    req.transaction_type = transaction_type
    return perform_transaction(account_oid, req)


@router.get("/transactions/")
def list_transactions_endpoint(
    account_id: str = Query(None, description="Mongo ObjectId of the account"),
    transaction_type: str = Query(None, description="Filter by credit/debit"),
):
    if transaction_type and transaction_type not in {"credit", "debit"}:
        raise HTTPException(status_code=422, detail="transaction_type must be credit or debit")

    return list_transactions(account_id=account_id, transaction_type=transaction_type)
