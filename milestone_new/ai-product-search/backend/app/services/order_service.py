from datetime import datetime, timezone

from app.domain.auth.schemas import UserSession
from app.domain.orders.schemas import CheckoutRequest, OrderResponse


class OrderService:
    def __init__(self, orders) -> None:
        self.orders = orders

    async def checkout(self, user: UserSession, payload: CheckoutRequest) -> OrderResponse:
        if not payload.items:
            raise ValueError("Cart is empty")
        total = sum(item.price * item.quantity for item in payload.items)
        order = {
            "order_id": f"ORD-{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "user_id": user.user_id,
            "username": user.username,
            "status": "PAID",
            "total": round(total, 2),
            "items": [item.model_dump() for item in payload.items],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        saved = await self.orders.create_order(order)
        return OrderResponse(**saved)

    async def list_orders(self, user: UserSession) -> list[OrderResponse]:
        rows = await self.orders.list_user_orders(user.user_id)
        return [OrderResponse(**row) for row in rows]
