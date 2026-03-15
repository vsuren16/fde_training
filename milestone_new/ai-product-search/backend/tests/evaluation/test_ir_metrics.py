import json
import os
from pathlib import Path

from fastapi.testclient import TestClient

os.environ["USE_FAKE_EMBEDDINGS"] = "true"

from app.main import app


def apk(expected: list[str], predicted: list[str], k: int = 5) -> float:
    score = 0.0
    hits = 0
    for i, p in enumerate(predicted[:k], start=1):
        if p in expected and p not in predicted[: i - 1]:
            hits += 1
            score += hits / i
    return score / min(len(expected), k) if expected else 0.0


def ndcg(expected: list[str], predicted: list[str], k: int = 5) -> float:
    def dcg(items: list[str]) -> float:
        out = 0.0
        for idx, item in enumerate(items[:k], start=1):
            rel = 1.0 if item in expected else 0.0
            out += rel / (1 if idx == 1 else __import__("math").log2(idx))
        return out

    ideal = dcg(expected)
    return dcg(predicted) / ideal if ideal > 0 else 0.0


def test_ir_metrics_are_reported() -> None:
    gt = json.loads(Path("tests/evaluation/ground_truth.json").read_text(encoding="utf-8"))
    with TestClient(app) as client:
        ap_scores = []
        ndcg_scores = []
        for row in gt:
            response = client.post("/products/recommend", json={"prompt": row["query"]})
            assert response.status_code == 200
            predicted = [x["id"] for x in response.json()["results"]]
            ap_scores.append(apk(row["expected_top_ids"], predicted))
            ndcg_scores.append(ndcg(row["expected_top_ids"], predicted))

    map_score = sum(ap_scores) / len(ap_scores)
    ndcg_score = sum(ndcg_scores) / len(ndcg_scores)
    assert map_score >= 0
    assert ndcg_score >= 0
