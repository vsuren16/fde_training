from fastapi import FastAPI

app = FastAPI(
    title="User Service",
    description="Handles user-related operations",
    version="1.0"
)

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
        "name": "Samatha"
    }
