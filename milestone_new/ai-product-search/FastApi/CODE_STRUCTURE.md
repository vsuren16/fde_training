# High-Level and Low-Level Code Structure

## High-Level Modules

- `app/main.py`: FastAPI bootstrap, middleware, startup lifecycle, repository/service wiring
- `app/api/routers`: API endpoints for products, recommendations, auth, chat, orders, health
- `app/services`: business orchestration for products, recommendations, ingestion, chat, auth, orders
- `app/infrastructure/embedding`: embedding provider implementations and model attribution manager
- `app/infrastructure/vector_store`: cosine-similarity vector retrieval via Chroma or in-memory fallback
- `app/infrastructure/db`: analytics persistence for search history
- `app/infrastructure/mongodb`: MongoDB product, user, and order repositories
- `app/domain`: request/response schemas and DTOs

## Low-Level Flow for Recommendations

1. Router accepts `POST /products/recommend`.
2. `RecommendationService` normalizes the query text.
3. `EmbeddingManager` embeds the query and returns:
   - vector
   - exact `model_version` used for that successful call
4. `VectorStore` performs nearest-neighbor retrieval using cosine similarity.
5. Service applies business filters:
   - availability
   - category
   - max price
6. Service ranks and truncates to top `K=5`.
7. Response is returned with:
   - normalized query
   - actual `model_version`
   - `latency_ms`
   - `assistant_response`
   - `results[]` including image URLs and similarity score
8. Search history is stored in SQLite for analytics.
9. Optional LangSmith trace captures request inputs, outputs, fallback usage, and model attribution.

## Static and Template Assets

- `app/static/css/style.css`: legacy stylesheet required by the submission template structure
- `app/static/js/cart.js`: legacy cart helper placeholder
- `app/templates/base.html`, `cart.html`, `index.html`: required template placeholders

## Compatibility Note

The authoritative runtime code is maintained in `../backend/app`. This `FastApi/` folder is intentionally shaped to satisfy the mandatory submission structure while pointing to the same implementation.
