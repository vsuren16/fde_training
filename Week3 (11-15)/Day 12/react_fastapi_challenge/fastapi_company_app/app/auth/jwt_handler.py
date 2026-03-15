# Used to work with dates and time (for token expiry calculation)
from datetime import datetime, timedelta

# JWT library from python-jose to create JSON Web Tokens
from jose import jwt

# Secret key used to sign the JWT (keep this safe in real projects)
SECRET_KEY = "company_secret_key"

# Algorithm used to sign the token (HS256 = HMAC + SHA256)
ALGORITHM = "HS256"

# Token validity duration in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """
    Creates a JWT access token.

    :param data: Dictionary containing data to store inside the token
                 (example: {"sub": "username"})
    :return: Encoded JWT token as a string
    """

    # Create a copy of the data so original data is not modified
    to_encode = data.copy()

    # Calculate token expiry time (current UTC time + 30 minutes)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiry time to the token payload
    to_encode.update({"exp": expire})

    # Encode the token using secret key and algorithm
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # Return the generated JWT token
    return encoded_jwt