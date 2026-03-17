from app.ingestion.resolution_enricher import infer_seed_category


def test_infer_seed_category_maps_database_terms() -> None:
    category = infer_seed_category(
        ci_category="database",
        ci_subcategory="Database",
        closure_code="Software",
    )

    assert category == "database"


def test_infer_seed_category_maps_storage_terms() -> None:
    category = infer_seed_category(
        ci_category="storage",
        ci_subcategory="SAN",
        closure_code="Other",
    )

    assert category == "storage"
