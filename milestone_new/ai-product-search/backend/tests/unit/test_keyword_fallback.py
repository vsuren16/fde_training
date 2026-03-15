from app.services.keyword_search_service import KeywordSearchService


def test_keyword_fallback_respects_top_k() -> None:
    service = KeywordSearchService()
    products = [
        {"id": "1", "product_name": "Temple Kurta", "short_description": "temple", "description": "traditional", "category": "traditional", "brand": "A", "price": 1000, "image_url": "a", "availability": True},
        {"id": "2", "product_name": "Office Blazer", "short_description": "office", "description": "formal", "category": "formal", "brand": "B", "price": 2000, "image_url": "b", "availability": True},
    ]
    results = service.rank("temple outfit", products, 1)
    assert len(results) == 1
    assert results[0]["id"] == "1"
