from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.rag_service import generate_rag_response


router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str


@router.post("")
async def chat(request: ChatRequest):
    return generate_rag_response(request.question)
