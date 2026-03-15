# Base class for creating Pydantic models
from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Request body schema for creating a new user.
    Used mainly during registration or admin user creation.
    """

    # Username for the user
    username: str

    # Plain text password (will be hashed before saving)
    password: str

    # Role assigned to the user (example: "admin", "user")
    role: str


class UserResponse(BaseModel):
    """
    Response schema for returning user details.
    Sensitive fields like password are excluded.
    """

    # User ID from database
    id: int

    # Username of the user
    username: str

    # Role of the user
    role: str

    class Config:
        # Allows Pydantic to work directly with SQLAlchemy ORM objects
        orm_mode = True