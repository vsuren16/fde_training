from pydantic import BaseModel, Field


class Review(BaseModel):
    user: str
    comment: str
    rating: float = Field(ge=1, le=5)


class ProductDimensions(BaseModel):
    length_cm: float = Field(gt=0)
    width_cm: float = Field(gt=0)
    height_cm: float = Field(gt=0)


class ProductBase(BaseModel):
    product_name: str = Field(min_length=2, max_length=140)
    short_description: str = Field(min_length=5, max_length=240)
    description: str = Field(min_length=10, max_length=1200)
    category: str = Field(min_length=2, max_length=80)
    brand: str = Field(min_length=2, max_length=80)
    color: str = Field(min_length=2, max_length=40)
    size: str = Field(min_length=1, max_length=20)
    price: float = Field(gt=0)
    image_url: str = Field(min_length=3)
    image_urls: list[str] = Field(default_factory=list)
    rating: float = Field(ge=1, le=5)
    dimensions: ProductDimensions
    availability: bool = True
    reviews: list[Review] = Field(default_factory=list)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: str


class ProductListResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    items: list[ProductResponse]
    facets: dict[str, list[str]]
