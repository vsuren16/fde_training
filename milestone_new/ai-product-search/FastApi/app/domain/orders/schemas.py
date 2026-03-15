from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    id: str
    product_name: str
    price: float = Field(ge=0)
    quantity: int = Field(default=1, ge=1)
    image_url: str | None = None


class CheckoutRequest(BaseModel):
    items: list[OrderItem] = Field(default_factory=list)


class OrderResponse(BaseModel):
    order_id: str
    user_id: str
    username: str
    status: str
    total: float
    items: list[OrderItem]
    created_at: str

