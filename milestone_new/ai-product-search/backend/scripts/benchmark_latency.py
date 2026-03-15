import statistics
import time
import logging
import os
from fastapi.testclient import TestClient

os.environ["USE_FAKE_EMBEDDINGS"] = "true"

from app.main import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("benchmark")


if __name__ == "__main__":
    client = TestClient(app)
    latencies = []
    for _ in range(100):
        start = time.perf_counter()
        response = client.post("/products/recommend", json={"prompt": "suggest traditional temple outfit"})
        response.raise_for_status()
        latencies.append((time.perf_counter() - start) * 1000)
    p99 = statistics.quantiles(latencies, n=100)[98]
    logger.info(
        "latency_benchmark",
        extra={"p99_ms": round(p99, 2), "avg_ms": round(sum(latencies) / len(latencies), 2)},
    )
