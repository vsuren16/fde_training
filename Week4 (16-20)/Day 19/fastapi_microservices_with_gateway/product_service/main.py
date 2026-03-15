from fastapi import FastAPI

app = FastAPI(
    title="Product Service",
    description="Handles product-related operations",
    version="1.0"
)

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {
        "product_id": product_id,
        "name": "Laptop",
        "price": 75000
    }
