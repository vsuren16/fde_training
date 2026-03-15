# Future Interfaces (Locked for Milestones 2-4)

This document defines interfaces and metadata contracts reserved for later milestones. These are **not implemented** yet.

## JWT Claims Contract (M2)
```json
{
  "sub": "user_email_or_subject",
  "user_id": "uuid-string",
  "role": "customer|admin",
  "iat": 1700000000,
  "exp": 1700007200,
  "token_version": 1
}
```

## Product + Inventory Join Expectation (M2)
- Join key: `products.product_id = inventory.product_id`
- Product service stock-aware response should include:
```json
{
  "product_id": "P-101",
  "title": "...",
  "price": 0,
  "inventory": {
    "available_stock": 0,
    "reserved_stock": 0,
    "damaged_stock": 0,
    "reorder_level": 0,
    "last_updated": "ISO-8601"
  }
}
```

## Semantic Search API Schema (M3)
### Request
```json
{
  "query": "comfortable running shoes under 5000",
  "filters": {
    "category": "shoes",
    "min_price": 1000,
    "max_price": 5000
  },
  "top_k": 5
}
```

### Response
```json
{
  "answer_text": "...",
  "recommended_products": ["P-101", "P-102"],
  "citations": ["P-101", "P-102"],
  "confidence": 0.91,
  "model_version": "sentence-transformers/all-MiniLM-L6-v2",
  "embedding_version": "emb-v1"
}
```

## Version Metadata Fields (M4)
### Product Embedding Metadata
```json
{
  "embedding_vector": [0.1, 0.2, 0.3],
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "embedding_version": "emb-v1",
  "embedding_generated_at": "ISO-8601"
}
```

### Search Trace / LLM Ops Log Metadata
```json
{
  "request_id": "uuid",
  "trace_id": "uuid",
  "query_text": "...",
  "prompt_version": "prompt-v1",
  "model_version": "model-v1",
  "embedding_version": "emb-v1",
  "timestamp": "ISO-8601"
}
```
