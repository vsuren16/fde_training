from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

from app.services.chatbot_service import handle_chat

router = APIRouter(tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    product_id: Optional[str] = None

@router.post("/chat")
async def chat(req: ChatRequest):
    return await handle_chat(message=req.message, product_id=req.product_id)