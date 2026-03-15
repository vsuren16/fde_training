# AI-Powered Outfit Recommendation Platform

## 1. Project Objective

Build a simplified AI-powered outfit recommendation system using FastAPI. Users submit natural language prompts such as `Suggest the best outfit to wear to temple`, and the system returns relevant outfit recommendations with product images, metadata, and similarity scores using semantic search.

## 2. Learning Outcomes Covered

- Understand traditional e-commerce product listing systems
- Design and build structured FastAPI backend applications
- Implement semantic search using embeddings
- Apply cosine similarity ranking
- Return contextual recommendations with images and metadata
- Track model versions and log AI usage

## 3. System Architecture Overview

```text
User Prompt -> FastAPI -> Query Embedding -> Cosine Similarity Ranking -> Top Outfit Recommendations
```

## 4. Mandatory Project Structure

The repository includes a literal submission tree under `FastApi/` to match the required structure:

```text
ai-product-search/
+-- FastApi/
    +-- README.md
    +-- CODE_STRUCTURE.md
    +-- DESIGN_DECISIONS.md
    +-- API_DOCUMENTATION.md
    +-- requirements.txt
    +-- app/
        +-- main.py
        +-- __init__.py
        +-- static/
        ¦   +-- css/style.css
        ¦   +-- images/
        ¦   +-- js/cart.js
        +-- templates/
            +-- base.html
            +-- cart.html
            +-- index.html
```

## 5. API Requirements Implemented

Product APIs:
- `GET /products`
- `GET /products/{id}`
- `POST /products`

AI Recommendation API:
- `POST /products/recommend`
- Request body: `{ "prompt": "User natural language query" }`
- Response includes:
  - normalized query text
  - exact embedding `model_version` used for the request
  - `latency_ms`
  - top 5 recommended products
  - image URLs
  - similarity score

## 6. Semantic Search Implementation

### 6.1 Indexing Phase
- Product embeddings are generated using the configured embedding provider chain.
- Exact embedding dimensions are enforced by the vector store.
- Product vectors are stored in ChromaDB, with in-memory fallback for development.
- Metadata stored with each vector includes product ID, category, image URL, price, and embedding model version.

### 6.2 Online Query Phase
- User query text is normalized.
- The same embedding pipeline generates the query embedding.
- The exact model version used for the successful embedding call is captured.

### 6.3 Similarity Search
- Nearest-neighbor retrieval is performed through the vector-store abstraction.
- Cosine similarity is used for ranking.

### 6.4 Ranking and Business Filtering
- Results are ranked by similarity score.
- Business filters supported include availability, category, and max price.
- Keyword fallback is used if semantic retrieval is unavailable.

### 6.5 Response Construction
- Top 5 results are returned.
- Product metadata and image URLs are included.
- The API response is frontend-ready.

## 7. Logging and Model Version Tracking

Implemented:
- log user query
- log exact embedding model version used for the request
- log latency and similarity scores
- store search history for analytics
- optional LangSmith tracing for recommendation runs

## 8. Optional Enhancements Implemented

- Hybrid keyword plus semantic fallback
- MongoDB integration for products, users, and orders
- Chroma-based vector storage
- Optional LangSmith observability and tracing

## 9. One-Command Docker Startup

From the repository root:

```bash
docker compose up --build
```

Services exposed:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8050`
- Backend Docs: `http://localhost:8050/docs`
- MongoDB: `mongodb://localhost:27017`

Docker artifacts provided:
- `docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`

## 10. Local Development Run

Backend:
```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8050
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Submission-facing structure:
- `FastApi/` contains the requirement-aligned tree and documentation.
- `backend/` and `frontend/` contain the working development layout.
