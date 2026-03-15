# Secret key used to sign and verify JWT tokens
# IMPORTANT: This should NOT be hardcoded in real applications
# It must be moved to an environment variable (.env file) later
SECRET_KEY = "SECRET123"

# Algorithm used to sign the JWT token
# HS256 = HMAC using SHA-256 (symmetric encryption)
ALGORITHM = "HS256"

# Access token expiry time in minutes
# After this time, the user must login again
ACCESS_TOKEN_EXPIRE_MINUTES = 30