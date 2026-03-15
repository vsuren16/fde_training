from fastapi import APIRouter, Body, HTTPException, Path, Query

from customers import customers_db

router = APIRouter(prefix="/transactions", tags=["transactions"])

transactions_db: dict[int, dict] = {}

@router.post("/{transaction_id}")
def create_transaction(
    transaction_id: int = Path(..., gt=0, description="Transaction ID must be > 0"),
    customer_id: int = Query(..., gt=0, description="Customer ID must be > 0 and must exist"),
    transaction_type: str = Query(..., description="Transaction type must be one of: deposit, withdraw"),
    amount: float = Body(..., gt=0, embed=True),
):
    if transaction_id in transactions_db:
        raise HTTPException(
            status_code=409,
            detail=f"Transaction with transaction_id={transaction_id} already exists.",
        )

    # Customer must exist
    if customer_id not in customers_db:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with customer_id={customer_id} not found.",
        )

    # Validate transaction type via query parameter
    allowed_types = {"deposit", "withdraw"}
    if transaction_type not in allowed_types:
        raise HTTPException(
            status_code=422,
            detail="Invalid transaction_type. Allowed values: deposit, withdraw.",
        )

    # Apply business rules + update balance
    current_balance = float(customers_db[customer_id]["balance"])

    if transaction_type == "withdraw":
        # Withdrawal amount must not exceed balance
        if amount > current_balance:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient balance. Current balance is {current_balance}.",
            )
        new_balance = current_balance - amount
    else:
        new_balance = current_balance + amount

    customers_db[customer_id]["balance"] = new_balance

    transactions_db[transaction_id] = {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "transaction_type": transaction_type,
        "amount": float(amount),
        "balance_after": new_balance,
    }

    return {
        "message": "Transaction created successfully.",
        "transaction": transactions_db[transaction_id],
    }


@router.get("/{transaction_id}")
def read_transaction(
    transaction_id: int = Path(..., gt=0, description="Transaction ID must be > 0"),
):
    if transaction_id not in transactions_db:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction with transaction_id={transaction_id} not found.",
        )

    return {"transaction": transactions_db[transaction_id]}


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int = Path(..., gt=0, description="Transaction ID must be > 0"),
):
    """
    Deletes a transaction record only.
    Note: We do NOT roll back balances here (not required by the prompt).
    """
    if transaction_id not in transactions_db:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction with transaction_id={transaction_id} not found.",
        )

    deleted = transactions_db.pop(transaction_id)
    return {"message": "Transaction deleted successfully.", "transaction": deleted}
