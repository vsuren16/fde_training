import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"
LOG_DIR = BASE_DIR / "logs"
TEMPLATES_DIR = BASE_DIR / "templates"

PRODUCTS_FILE = DATA_DIR / "products.json"
CHUNKS_FILE = STORAGE_DIR / "chunks.json"
EMBEDDINGS_FILE = STORAGE_DIR / "embeddings.npy"
FAISS_INDEX_FILE = STORAGE_DIR / "faiss.index"
EVAL_LOG_FILE = LOG_DIR / "evaluation_log.jsonl"

EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
RERANK_MODEL_NAME = os.getenv("RERANK_MODEL_NAME", "cross-encoder/ms-marco-MiniLM-L-6-v2")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_JUDGE_MODEL = os.getenv("OPENAI_JUDGE_MODEL", "gpt-4.1-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

VECTOR_DIM = 384
TOP_K_RETRIEVE = 20
TOP_K_RERANK = 5
CHUNK_SIZE = 380
CHUNK_OVERLAP = 50
OPENAI_TIMEOUT_SECONDS = 20.0
ENABLE_JUDGE_DEFAULT = True

for path in [DATA_DIR, STORAGE_DIR, LOG_DIR, TEMPLATES_DIR]:
    path.mkdir(parents=True, exist_ok=True)
