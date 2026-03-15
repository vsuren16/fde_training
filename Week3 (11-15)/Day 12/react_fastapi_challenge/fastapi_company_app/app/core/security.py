# Used for dependency injection and HTTP error handling
from fastapi import Depends, HTTPException, status

# Used to read Authorization header (Bearer token)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# JWT utilities for decoding and error handling
from jose import jwt, JWTError

# Import secret key and algorithm used to verify JWT
from app.auth.jwt_handler import SECRET_KEY, ALGORITHM


# Creates the "Authorize" button in Swagger UI
# This tells FastAPI to expect a Bearer token in Authorization header
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Extracts and validates JWT token from Authorization header.

    Flow:
    - Reads Bearer token from request
    - Decodes and verifies the JWT
    - Returns user data stored inside token
    """

    # If no credentials are provided
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization required"
        )

    # Extracts the token value (removes 'Bearer ' part automatically)
    token = credentials.credentials

    try:
        # Decode the JWT token using secret key and algorithm
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Payload usually contains user info like username, role, etc.
        return payload

    except JWTError:
        # Raised when token is invalid, expired, or tampered
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def admin_only(user: dict = Depends(get_current_user)):
    """
    Allows access only if the logged-in user has admin role.
    """

    # Check user role from token payload
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    # If role is admin, allow request to proceed
    return user