from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.dependencies.auth import get_current_user
from app.domain.orders.schemas import CheckoutRequest, OrderResponse

router = APIRouter(prefix="/orders")


@router.get("", response_model=list[OrderResponse])
async def list_orders(request: Request, current_user=Depends(get_current_user)):
    return await request.app.state.container.order_service.list_orders(current_user)


@router.get("/me", response_model=list[OrderResponse])
async def my_orders(request: Request, current_user=Depends(get_current_user)):
    return await request.app.state.container.order_service.list_orders(current_user)


@router.post("/checkout", response_model=OrderResponse)
async def checkout(payload: CheckoutRequest, request: Request, current_user=Depends(get_current_user)):
    try:
        return await request.app.state.container.order_service.checkout(current_user, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
