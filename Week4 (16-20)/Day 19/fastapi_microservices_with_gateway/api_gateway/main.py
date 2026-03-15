from fastapi import FastAPI
import httpx

app = FastAPI(
    title="API Gateway",
    description="Gateway for User and Product Services",
    version="1.0"
)

USER_SERVICE_URL = "http://127.0.0.1:8001"
PRODUCT_SERVICE_URL = "http://127.0.0.1:8002"

@app.get("/users/{user_id}")
async def gateway_get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
    return response.json()

@app.get("/products/{product_id}")
async def gateway_get_product(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    return response.json()

'''
from fastapi import HTTPException
import httpx

@app.get("/users/{user_id}")
async def gateway_get_user(user_id: int):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{USER_SERVICE_URL}/users/{user_id}"
            )
            response.raise_for_status()
        return response.json()

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="User service is unavailable"
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.text
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error in API Gateway"
        )


@app.get("/products/{product_id}")
async def gateway_get_product(product_id: int):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{PRODUCT_SERVICE_URL}/products/{product_id}"
            )
            response.raise_for_status()
        return response.json()

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Product service is unavailable"
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.text
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error in API Gateway"
        )
'''