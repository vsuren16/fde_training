from pathlib import Path


def test_future_service_scaffolds_present():
    root = Path(__file__).resolve().parents[1]
    targets = [
        root / "services" / "api-gateway" / "app" / "main.py",
        root / "services" / "user-service" / "app" / "main.py",
        root / "services" / "product-service" / "app" / "main.py",
        root / "services" / "cart-service" / "app" / "main.py",
        root / "services" / "order-service" / "app" / "main.py",
        root / "services" / "search-service" / "app" / "main.py",
    ]

    for path in targets:
        content = path.read_text(encoding="utf-8")
        assert "Not Implemented in Milestone 1" in content
