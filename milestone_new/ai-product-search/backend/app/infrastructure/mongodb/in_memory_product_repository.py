from app.domain.products.schemas import ProductCreate, ProductResponse


class InMemoryProductRepository:
    def __init__(self) -> None:
        self.items: list[dict] = []

    async def create_indexes(self) -> None:
        return

    async def count(self) -> int:
        return len(self.items)

    async def bulk_insert(self, products: list[dict]) -> None:
        self.items.extend(products)

    async def sync_seed_catalog(self, products: list[dict]) -> int:
        by_id = {item["id"]: item for item in self.items}
        updated = 0
        for product in products:
            product_id = product.get("id")
            if product_id in by_id:
                by_id[product_id].update(product)
            else:
                self.items.append(product)
            updated += 1
        return updated

    async def create(self, payload: ProductCreate) -> ProductResponse:
        item = {"id": f"p-{100000 + len(self.items)}", **payload.model_dump()}
        self.items.append(item)
        return ProductResponse(**item)

    async def get_by_id(self, product_id: str) -> ProductResponse | None:
        for item in self.items:
            if item["id"] == product_id:
                return ProductResponse(**item)
        return None

    async def list_paginated(self, filters: dict, page: int, page_size: int) -> tuple[list[ProductResponse], int]:
        rows = list(self.items)
        if filters.get("category"):
            rows = [x for x in rows if x["category"] == filters["category"]]
        if filters.get("brand"):
            rows = [x for x in rows if x["brand"] == filters["brand"]]
        if filters.get("color"):
            rows = [x for x in rows if x["color"] == filters["color"]]
        if filters.get("size"):
            rows = [x for x in rows if x["size"] == filters["size"]]
        if filters.get("availability") is not None:
            rows = [x for x in rows if x["availability"] == filters["availability"]]
        if filters.get("min_price") is not None:
            rows = [x for x in rows if x["price"] >= filters["min_price"]]
        if filters.get("max_price") is not None:
            rows = [x for x in rows if x["price"] <= filters["max_price"]]
        if filters.get("search"):
            s = filters["search"].lower()
            rows = [x for x in rows if s in x["product_name"].lower() or s in x["description"].lower()]
        total = len(rows)
        start = (page - 1) * page_size
        paged = rows[start : start + page_size]
        return [ProductResponse(**x) for x in paged], total

    async def list_all(self) -> list[ProductResponse]:
        return [ProductResponse(**x) for x in self.items]

    async def facet_values(self) -> dict[str, list[str]]:
        return {
            "brands": sorted(set(x["brand"] for x in self.items)),
            "categories": sorted(set(x["category"] for x in self.items)),
            "colors": sorted(set(x["color"] for x in self.items)),
            "sizes": sorted(set(x["size"] for x in self.items)),
        }
