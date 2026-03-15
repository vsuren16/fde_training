# Requirements Snapshot

Original objective: Build FastAPI AI-commerce backend with semantic outfit recommendations from natural language prompts.

Mandatory APIs:
- GET /products
- GET /products/{id}
- POST /products
- POST /products/recommend

Required recommendation response fields:
- query text
- model version
- top 5 products
- image URLs
- similarity score
