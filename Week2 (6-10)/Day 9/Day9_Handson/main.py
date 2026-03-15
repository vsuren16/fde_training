import time
import bcrypt
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "mysecretkey"
ALGO = "HS256"

users: dict[str, dict] = {}

# -----------------------------
# Step 1: Signup
# -----------------------------
def signup(username: str, password: str, role: str) -> None:
    if username in users:
        raise ValueError(f"User '{username}' already exists")

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users[username] = {"password_hash": password_hash, "role": role}

    print(f" Signed up: {username}")
    print(f"   Stored hash: {password_hash}")
    print(f"   Stored role: {role}")

# -----------------------------
# Step 2: Login + JWT issuance
# -----------------------------
def login(username: str, password: str) -> str | None:
    user = users.get(username)
    if not user:
        print(f" Login failed: user '{username}' not found")
        return None

    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
        print(f" Login failed: invalid password for '{username}'")
        return None

    payload = {
        "sub": username,
        "role": user["role"],
        "exp": int(time.time()) + 60,  # 60 seconds expiry
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)
    print(f" Login successful: {username}")
    print(f"   JWT token: {token}")
    return token


# -----------------------------
# Step 3: Decode + Authorization helper
# -----------------------------
def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        return payload
    except ExpiredSignatureError:
        print("Token expired")
        return None
    except InvalidTokenError:
        print("Invalid token")
        return None


def require_role(token: str, allowed_roles: list[str]) -> dict | None:
    payload = decode_token(token)
    if not payload:
        return None

    if payload.get("role") in allowed_roles:
        print("Access granted")
        return payload

    print("Access denied")
    return None

# -----------------------------
# Step 4: Fake protected endpoints
# -----------------------------
def delete_user(token: str, username_to_delete: str) -> None:
    payload = require_role(token, ["admin"])
    if not payload:
        print("Forbidden")
        return
    print(f"User {username_to_delete} deleted")


def view_profile(token: str) -> None:
    payload = require_role(token, ["admin", "user"])
    if not payload:
        print("Forbidden")
        return
    print(f"Showing profile for {payload['sub']}")
