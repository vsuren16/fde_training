from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    CHUNKS_FILE,
    EMBED_MODEL_NAME,
    EMBEDDINGS_FILE,
    EVAL_LOG_FILE,
    FAISS_INDEX_FILE,
    PRODUCTS_FILE,
    RERANK_MODEL_NAME,
    TEMPLATES_DIR,
    TOP_K_RETRIEVE,
    VECTOR_DIM,
)
from evaluation.judge import Judge
from evaluation.metrics_store import MetricsStore
from generation.llm_generator import LLMGenerator
from ingestion.chunker import Chunker
from ingestion.embedder import Embedder
from ingestion.loader import ProductLoader
from orchestration.pipeline import EcommercePipeline
from retrieval.reranker import Reranker
from retrieval.retriever import Retriever
from retrieval.vector_store import VectorStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    judge_enabled: bool = True


class SearchResponse(BaseModel):
    products: list[dict]
    llm_explanation: str
    evaluation_score: dict
    pre_rerank_order: list[int | None]
    post_rerank_order: list[int | None]


templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def build_pipeline() -> EcommercePipeline:
    loader = ProductLoader(PRODUCTS_FILE)
    products = loader.load()

    chunker = Chunker(chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    chunks = chunker.chunk_products(products)

    embedder = Embedder(EMBED_MODEL_NAME, EMBEDDINGS_FILE, CHUNKS_FILE)
    cached_chunks, embeddings = embedder.build_or_load(chunks)

    vector_store = VectorStore(dim=VECTOR_DIM, index_path=FAISS_INDEX_FILE)
    vector_store.build_or_load(embeddings)

    retriever = Retriever(embedder=embedder, vector_store=vector_store, chunks=cached_chunks, top_k=TOP_K_RETRIEVE)
    reranker = Reranker(model_name=RERANK_MODEL_NAME)
    generator = LLMGenerator()
    judge = Judge()
    metrics_store = MetricsStore(EVAL_LOG_FILE)

    return EcommercePipeline(
        retriever=retriever,
        reranker=reranker,
        generator=generator,
        judge=judge,
        metrics_store=metrics_store,
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Initializing semantic search pipeline...")
    app.state.pipeline = build_pipeline()
    logger.info("Pipeline ready.")
    yield


app = FastAPI(title="AI E-Commerce Semantic Search", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    pipeline: EcommercePipeline = app.state.pipeline
    pipeline.set_judge_enabled(request.judge_enabled)
    result = await pipeline.run(request.query)
    return {
        "products": result["products"],
        "llm_explanation": result["llm_explanation"],
        "evaluation_score": result["evaluation_score"],
        "pre_rerank_order": result["pre_rerank_order"],
        "post_rerank_order": result["post_rerank_order"],
    }


@app.get("/metrics")
async def metrics():
    pipeline: EcommercePipeline = app.state.pipeline
    return pipeline.metrics_store.summary()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8010, reload=True)
