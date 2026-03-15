import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

SERVICE_NAME = os.getenv("SERVICE_NAME", "cart-service")

app = FastAPI(title=f"{SERVICE_NAME} (Scaffold)", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "scaffold", "milestone": "future", "service": SERVICE_NAME}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def not_implemented(path: str, request: Request):
    return JSONResponse(
        status_code=501,
        content={
            "detail": "Not Implemented in Milestone 1",
            "service": SERVICE_NAME,
            "method": request.method,
            "path": f"/{path}",
            "planned_milestones": ["M2", "M3", "M4"],
        },
    )
