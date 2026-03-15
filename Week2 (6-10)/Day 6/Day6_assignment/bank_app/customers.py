import re
from fastapi import APIRouter, Body, HTTPException, Path, Query

router = APIRouter(prefix="/customers", tags=["customers"])

customers_db: dict[int, dict] = {}

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

@router.post("/{customer_id}")
def create_customer(
    customer_id: int = Path(..., gt=0, description="Customer ID must be > 0"),
    account_type: str = Query(..., description="Account type must be one of: savings, current"),
    name: str = Body(..., min_length=3, embed=True),
    balance: float = Body(..., ge=0, embed=True),
    email: str = Body(..., embed=True),
):
    allowed_types = {"savings", "current"}
    if account_type not in allowed_types:
        raise HTTPException(
            status_code=422,
            detail="Invalid account_type. Allowed values: savings, current.",
        )

    if customer_id in customers_db:
        raise HTTPException(
            status_code=409,
            detail=f"Customer with customer_id={customer_id} already exists.",
        )

    if not EMAIL_REGEX.match(email):
        raise HTTPException(
            status_code=422,
            detail="Invalid email format.",
        )

    customers_db[customer_id] = {
        "customer_id": customer_id,
        "name": name,
        "balance": float(balance),
        "email": email,
        "account_type": account_type,
    }

    return {"message": "Customer created successfully.", "customer": customers_db[customer_id]}


@router.get("/{customer_id}")
def read_customer(
    customer_id: int = Path(..., gt=0, description="Customer ID must be > 0"),
):
    if customer_id not in customers_db:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with customer_id={customer_id} not found.",
        )
    return {"customer": customers_db[customer_id]}


@router.put("/{customer_id}")
def update_customer(
    customer_id: int = Path(..., gt=0, description="Customer ID must be > 0"),
    account_type: str = Query(..., description="Account type must be one of: savings, current"),
    name: str = Body(..., min_length=3, embed=True),
    balance: float = Body(..., ge=0, embed=True),
    email: str = Body(..., embed=True),
):
    if customer_id not in customers_db:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with customer_id={customer_id} not found.",
        )

    allowed_types = {"savings", "current"}
    if account_type not in allowed_types:
        raise HTTPException(
            status_code=422,
            detail="Invalid account_type. Allowed values: savings, current.",
        )

    if not EMAIL_REGEX.match(email):
        raise HTTPException(
            status_code=422,
            detail="Invalid email format.",
        )

    customers_db[customer_id].update(
        {
            "name": name,
            "balance": float(balance),
            "email": email,
            "account_type": account_type,
        }
    )

    return {"message": "Customer updated successfully.", "customer": customers_db[customer_id]}


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int = Path(..., gt=0, description="Customer ID must be > 0"),
):
    if customer_id not in customers_db:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with customer_id={customer_id} not found.",
        )

    deleted = customers_db.pop(customer_id)
    return {"message": "Customer deleted successfully.", "customer": deleted}
