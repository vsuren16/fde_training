class KeywordSearchService:
    def rank(self, query: str, products: list[dict], top_k: int) -> list[dict]:
        tokens = [token for token in query.lower().split() if token]
        if not tokens:
            return []
        ranked = []
        for product in products:
            searchable = (
                f"{product.get('product_name', '')} {product.get('short_description', '')} "
                f"{product.get('description', '')} {product.get('category', '')} {product.get('brand', '')}"
            ).lower()
            score = sum(1 for token in tokens if token in searchable) / len(tokens)
            if score > 0:
                ranked.append({
                    "id": product["id"],
                    "name": product.get("product_name", "Unknown Product"),
                    "product_name": product.get("product_name", "Unknown Product"),
                    "category": product["category"],
                    "price": product["price"],
                    "image_url": product["image_url"],
                    "image_urls": product.get("image_urls", []),
                    "short_description": product.get("short_description", ""),
                    "description": product.get("description", ""),
                    "brand": product.get("brand", ""),
                    "color": product.get("color", ""),
                    "size": product.get("size", ""),
                    "available": product.get("availability", True),
                    "similarity_score": round(float(score), 4),
                })
        ranked.sort(key=lambda x: x["similarity_score"], reverse=True)
        return ranked[:top_k]
