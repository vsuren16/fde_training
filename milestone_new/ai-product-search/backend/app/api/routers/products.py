from fastapi import APIRouter, HTTPException, Query, Request, status

from app.domain.products.schemas import ProductCreate, ProductListResponse, ProductResponse

router = APIRouter()


@router.get("", response_model=ProductListResponse)
async def list_products(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=9, ge=1, le=50),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    brand: str | None = None,
    category: str | None = None,
    color: str | None = None,
    size: str | None = None,
    availability: bool | None = None,
    search: str | None = None,
) -> ProductListResponse:
    return await request.app.state.container.product_service.list_products(
        page=page,
        page_size=page_size,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        category=category,
        color=color,
        size=size,
        availability=availability,
        search=search,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, request: Request) -> ProductResponse:
    product = await request.app.state.container.product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, request: Request) -> ProductResponse:
    product = await request.app.state.container.product_service.create_product(payload)
    await request.app.state.container.ingestion_service.build_index()
    return product

