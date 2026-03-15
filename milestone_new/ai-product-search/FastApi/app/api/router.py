from fastapi import APIRouter

from app.api.routers import auth, chat, health, orders, products, recommendations

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(orders.router, tags=["orders"])
api_router.include_router(chat.router, tags=["chat"])
# products MUST come before recommendations — both share prefix="/products"
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(recommendations.router, prefix="/products", tags=["recommendations"])

