from fastapi import FastAPI
from customers import router as customers_router
from transactions import router as transactions_router

app = FastAPI(title="Bank Management System")

app.include_router(customers_router)
app.include_router(transactions_router)

