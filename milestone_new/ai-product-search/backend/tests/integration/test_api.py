from fastapi.testclient import TestClient


def test_get_products_returns_seed_data(client: TestClient) -> None:
    response = client.get("/products")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total_items"] >= 3
    assert len(payload["items"]) > 0


def test_recommend_returns_model_version_and_scores(client: TestClient) -> None:
    response = client.post("/products/recommend", json={"prompt": "best outfit for temple"})
    assert response.status_code == 200
    payload = response.json()
    assert "model_version" in payload
    assert "results" in payload
    if payload["results"]:
        assert "similarity_score" in payload["results"][0]
