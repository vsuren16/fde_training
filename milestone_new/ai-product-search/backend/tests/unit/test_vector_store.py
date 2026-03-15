from app.infrastructure.vector_store.in_memory import InMemoryVectorStore


def test_cosine_ranking_returns_best_match_first() -> None:
    store = InMemoryVectorStore()
    store.build(
        embeddings=[[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]],
        payloads=[{"id": "a"}, {"id": "b"}, {"id": "c"}],
    )
    results = store.search([1.0, 0.1], 2)
    assert results[0]["id"] == "a"
    assert len(results) == 2
