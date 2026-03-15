# AI-Powered E-Commerce Semantic Search (No LangChain)

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.

## Run
```bash
uvicorn app:app --reload
```
Open: `http://127.0.0.1:8000`

## API
- `POST /search`
```json
{
  "query": "comfortable running shoes under 5000",
  "judge_enabled": true
}
```
- `GET /metrics`

## Notes
- FAISS index and cached embeddings persist in `storage/`.
- Evaluation logs are written to `logs/evaluation_log.jsonl`.
- RAG context is constrained to retrieved products only.
