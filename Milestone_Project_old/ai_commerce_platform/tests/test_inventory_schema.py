from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def test_inventory_schema_columns():
    schema_file = Path(__file__).resolve().parents[1] / "data-engineering" / "inventory_pipeline" / "schema.py"
    spec = spec_from_file_location("inventory_schema_module", schema_file)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    schema = module.inventory_schema()
    names = [field.name for field in schema.fields]
    assert names == [
        "inventory_id",
        "product_id",
        "warehouse_id",
        "available_stock",
        "reserved_stock",
        "damaged_stock",
        "reorder_level",
        "last_updated",
        "batch_number",
    ]
