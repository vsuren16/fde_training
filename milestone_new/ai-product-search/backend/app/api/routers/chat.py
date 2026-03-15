from fastapi import APIRouter, Header, Request

from app.api.dependencies.auth import parse_bearer_token
from app.domain.chat.schemas import ChatAskRequest, ChatAskResponse

router = APIRouter(prefix="/chat")


@router.post("/ask", response_model=ChatAskResponse)
async def ask_chatbot(
    payload: ChatAskRequest,
    request: Request,
    authorization: str | None = Header(default=None),
) -> ChatAskResponse:
    token = parse_bearer_token(authorization)
    user = request.app.state.container.auth_service.authenticate_token(token) if token else None
    return await request.app.state.container.chat_service.ask(payload.message, user=user)
