from fastapi import APIRouter, HTTPException, Request, status

from app.domain.auth.schemas import ForgotPasswordRequest, LoginRequest, LoginResponse, SignupRequest

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, request: Request):
    try:
        token, user = await request.app.state.container.auth_service.login(payload.username, payload.password)
        return LoginResponse(access_token=token, user=user)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/signup")
async def signup(payload: SignupRequest, request: Request):
    try:
        await request.app.state.container.auth_service.signup(payload.username, payload.password)
        return {"message": "Signup successful"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordRequest, request: Request):
    try:
        return await request.app.state.container.auth_service.forgot_password(payload.username)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
