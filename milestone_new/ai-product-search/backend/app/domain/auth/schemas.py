from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=120)
    password: str = Field(min_length=3, max_length=120)


class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=120)
    password: str = Field(min_length=6, max_length=120)


class ForgotPasswordRequest(BaseModel):
    username: str = Field(min_length=3, max_length=120)


class UserSession(BaseModel):
    user_id: str
    username: str
    role: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserSession
