import logging
import math

from app.domain.products.schemas import ProductCreate, ProductListResponse, ProductResponse
from app.infrastructure.mongodb.product_repository import MongoProductRepository
from app.seed.external_products import load_seed_products

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, repository: MongoProductRepository) -> None:
        self.repository = repository

    async def initialize(self) -> None:
        await self.repository.create_indexes()

    async def ensure_seed_data(self, count: int) -> None:
        docs = load_seed_products(count)
        existing = await self.repository.count()
        if existing > 0:
            if len(docs) != existing and hasattr(self.repository, "sync_seed_catalog"):
                updated = await self.repository.sync_seed_catalog(docs)
                if updated:
                    logger.info("seed_catalog_synced", extra={"count": updated})
            return
        await self.repository.bulk_insert(docs)
        logger.info("seed_products_inserted", extra={"count": count})

    async def list_products(
        self,
        page: int,
        page_size: int,
        min_price: float | None = None,
        max_price: float | None = None,
        brand: str | None = None,
        category: str | None = None,
        color: str | None = None,
        size: str | None = None,
        availability: bool | None = None,
        search: str | None = None,
    ) -> ProductListResponse:
        filters = {
            "min_price": min_price,
            "max_price": max_price,
            "brand": brand,
            "category": category,
            "color": color,
            "size": size,
            "availability": availability,
            "search": search,
        }
        items, total_items = await self.repository.list_paginated(filters, page, page_size)
        facets = await self.repository.facet_values()
        total_pages = max(1, math.ceil(total_items / page_size)) if page_size > 0 else 1
        return ProductListResponse(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            items=items,
            facets=facets,
        )

    async def list_all_products(self) -> list[ProductResponse]:
        return await self.repository.list_all()

    async def get_product(self, product_id: str) -> ProductResponse | None:
        return await self.repository.get_by_id(product_id)

    async def create_product(self, payload: ProductCreate) -> ProductResponse:
        return await self.repository.create(payload)

    async def product_documents(self) -> list[dict]:
        products = await self.list_all_products()
        docs: list[dict] = []
        for product in products:
            text = (
                f"{product.product_name} {product.short_description} "
                f"{product.description} {product.category} {product.brand} {product.color}"
            )
            docs.append(
                {
                    "id": product.id,
                    "text": text,
                    "metadata": {
                        "id": product.id,
                        "name": product.product_name,
                        "product_name": product.product_name,
                        "category": product.category,
                        "price": product.price,
                        "image_url": product.image_url,
                        "image_urls": product.image_urls,
                        "short_description": product.short_description,
                        "description": product.description,
                        "available": product.availability,
                        "brand": product.brand,
                        "color": product.color,
                        "size": product.size,
                    },
                }
            )
        return docs
