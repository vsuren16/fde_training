from typing import List, Dict, Any

from app.db.chroma import get_chroma_collection
from app.llm.embeddings import embed_text_async
from app.security.pii import sanitize_text_for_llm

async def semantic_search(query: str, top_k: int = 12) -> List[Dict[str, Any]]:
    """
    Returns Chroma hits with product_id + metadata + distance.
    """
    collection = get_chroma_collection()

    sanitized_query = sanitize_text_for_llm(query).sanitized_text or query
    qvec = await embed_text_async(sanitized_query)

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
