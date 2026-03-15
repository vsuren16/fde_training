# FastAPI utilities for routing, dependency injection, and error handling
from fastapi import APIRouter, Depends, HTTPException, status

# SQLAlchemy session for database operations
from sqlalchemy.orm import Session

# Database session dependency
from app.database import get_db

# User ORM model
from app.models import User

# Pydantic schemas for request validation
from app.schemas.auth_schema import RegisterRequest, LoginRequest

# Password hashing and verification utilities
from app.auth.password import hash_password, verify_password

# JWT token creation utility
from app.auth.jwt_handler import create_access_token


# Auth router
# tags=["auth"] groups these APIs under "auth" in Swagger UI
router = APIRouter(
    tags=["auth"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Registers a new user.

    Steps:
    - Check if username already exists
    - Hash the password
    - Save user to database
    """

    # Check if user with same username already exists
    existing_user = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Create new user object
    user = User(
        username=data.username,
        hashed_password=hash_password(data.password),  # hash password before saving
        role=data.role
    )

    # Save user to database
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticates a user and returns a JWT access token.

    Steps:
    - Fetch user from database
    - Verify password
    - Generate JWT token
    """

    # Fetch user by username
    user = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    # Validate username and password
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create JWT access token with user details
    access_token = create_access_token(
        data={
            "sub": user.username,  # subject (logged-in user)
            "role": user.role      # used for authorization
        }
    )

    # Return token in standard OAuth2 format
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }