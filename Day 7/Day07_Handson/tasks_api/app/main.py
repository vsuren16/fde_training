from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as tasks_router
app = FastAPI(title="Kanban Tickets Mongo API")
app.add_middleware(
 CORSMiddleware,
 allow_origins=["*"],
 allow_methods=["*"],
 allow_headers=["*"],
)
app.include_router(tasks_router)
