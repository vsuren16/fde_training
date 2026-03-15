# API Documentation

## Product APIs

### GET /products
Returns paginated products.

Query parameters supported:
- `page`
- `page_size`
- `min_price`
- `max_price`
- `brand`
- `category`
- `color`
- `size`
- `availability`
- `search`

### GET /products/{id}
Returns one product by id.

### POST /products
Creates a new product.

## AI Recommendation API

### POST /products/recommend

Request body:
```json
{
  "prompt": "Suggest the best outfit to wear to temple"
}
```

Optional filters:
```json
{
  "prompt": "Suggest elegant outfits for women",
  "category": "party",
  "max_price": 5000
}
```

Response shape:
```json
{
  "query": "suggest elegant outfits for women",
  "model_version": "local:sentence-transformers/all-MiniLM-L6-v2",
  "latency_ms": 64.12,
  "assistant_response": "Here are my top picks...",
  "results": [
    {
      "id": "p-610",
      "name": "Black One-Shoulder Gown",
      "product_name": "Black One-Shoulder Gown",
      "category": "party",
      "price": 4600.0,
      "image_url": "https://...",
      "image_urls": ["https://..."],
      "short_description": "Elegant one-shoulder evening gown...",
      "description": "Elegant one-shoulder evening gown...",
      "brand": "FabricHouse",
      "color": "black",
      "size": "M",
      "available": true,
      "similarity_score": 0.5989
    }
  ]
}
```

## Logging and Analytics

Each recommendation request stores:
- normalized query text
- exact embedding `model_version`
- latency in milliseconds
- top similarity scores

## Health APIs

- `GET /health/live`
- `GET /health/ready`

## LangSmith Tracing

When enabled through environment variables, recommendation requests are traced with:
- prompt inputs
- business filter inputs
- configured model chain
- actual model version used
- fallback usage
- result count and latency
