# Base class for Pydantic models (used for request validation)
from pydantic import BaseModel

# Literal restricts allowed values
from typing import Literal


class RegisterRequest(BaseModel):
    """
    Request body schema for user registration.
    Validates incoming data before it reaches the API logic.
    """

    # Username for the new user
    username: str

    # Plain text password (will be hashed before storing)
    password: str

    # Role of the user
    # Literal ensures only "admin" or "user" is allowed
    role: Literal["admin", "user"]

    class Config:
        # Forbid extra fields not defined in this schema
        # Example: sending "email" will raise a validation error
        extra = "forbid"


class LoginRequest(BaseModel):
    """
    Request body schema for user login.
    """

    # Username entered during login
    username: str

    # Password entered during login
    password: str

    class Config:
        # Rejects any extra fields in login request
        extra = "forbid"