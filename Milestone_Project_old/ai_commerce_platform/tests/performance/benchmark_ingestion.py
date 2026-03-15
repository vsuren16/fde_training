"""Simple ingestion benchmark runner for latency and throughput evidence."""

from __future__ import annotations

import json
import logging
import subprocess
import sys
import time
from statistics import quantiles
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='{"level":"%(levelname)s","message":"%(message)s"}')
logger = logging.getLogger("benchmark")


def run_once() -> float:
    start = time.perf_counter()
    repo_root = Path(__file__).resolve().parents[2]
    script_path = repo_root / "data-engineering" / "inventory_pipeline" / "spark_job.py"
    subprocess.run(
        [sys.executable, str(script_path), "--run-id", f"benchmark_{int(start * 1000)}"],
        check=True,
        cwd=str(repo_root),
    )
    return time.perf_counter() - start


def main():
    samples = []
    for _ in range(3):
        samples.append(run_once())

    p99 = quantiles(samples, n=100)[98] if len(samples) >= 2 else samples[0]
    throughput = 20 / (sum(samples) / len(samples))

    report = {
        "runs": len(samples),
        "durations_seconds": samples,
        "p99_seconds": p99,
        "estimated_records_per_second": throughput,
        "records_per_run": 20,
    }
    logger.info("benchmark_report %s", json.dumps(report))


if __name__ == "__main__":
    main()
