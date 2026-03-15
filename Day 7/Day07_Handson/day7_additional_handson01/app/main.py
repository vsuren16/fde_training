from fastapi import FastAPI
from .routes import router as bank_router

app = FastAPI(title="Bank Mongo API")

app.include_router(bank_router)
