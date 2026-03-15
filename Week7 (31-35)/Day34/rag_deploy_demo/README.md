# RAG Deploy Demo

Simple RAG demo with a FastAPI backend and a Vite + React frontend.

## Project structure

- `backend/` contains the API, retrieval logic, and dummy data.
- `frontend/` contains the React UI.
- `tests/` contains a small backend smoke test.

## Run backend

```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8010
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

## Environment

Use `.env.example` as the reference for your local `.env`. The real `.env` is ignored by Git.
