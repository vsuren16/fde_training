import os
from typing import List, Dict, Any
from openai import AsyncOpenAI
from app.db.chroma import get_chroma_collection

OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

async def semantic_search(query: str, top_k: int = 12) -> List[Dict[str, Any]]:
    """
    Returns Chroma hits with product_id + metadata + distance.
    """
    collection = get_chroma_collection()

    client = AsyncOpenAI()  # uses OPENAI_API_KEY from env
    emb = await client.embeddings.create(model=OPENAI_EMBED_MODEL, input=[query])
    qvec = emb.data[0].embedding

    res = collection.query(
        query_embeddings=[qvec],
        n_results=top_k,
        include=["metadatas", "distances", "documents", "ids"],
    )

    hits = []
    ids = res.get("ids", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    for pid, meta, dist in zip(ids, metas, dists):
        hits.append({
            "product_id": meta.get("product_id") or pid,
            "metadata": meta,
            "distance": dist,
        })
    return hits