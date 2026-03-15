from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.logging import setup_logging
from app.core.errors import unhandled_exception_handler
from app.db.mongodb import connect_mongo, close_mongo

from app.routers.health import router as health_router
from app.routers.products import router as products_router
from app.routers.insights import router as insights_router
from app.routers.search import router as search_router
from app.routers.chat import router as chat_router

from app.routers.recommendations import router as recommendations_router


setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await connect_mongo()
    yield
    # Shutdown logic
    await close_mongo()

app = FastAPI(
    title="GenAI E-Commerce Backend",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(health_router)
app.include_router(products_router)

app.include_router(insights_router)

app.include_router(search_router)

app.include_router(chat_router)

app.include_router(recommendations_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('app.main:app', host="0.0.0.0", port=8010)


