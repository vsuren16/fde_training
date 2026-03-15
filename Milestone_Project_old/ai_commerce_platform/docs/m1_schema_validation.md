# Milestone 1 - Inventory Schema Validation

## Source
- Source type: In-script mock dataset
- Raw records: 20
- Data quality: intentionally noisy/unstructured

## Examples of Raw Data Issues Included
- inconsistent column names (`inventory_id`, `inv_id`, `inventory`, `product id`, `warehouseId`)
- whitespace and mixed casing in identifiers
- numeric fields as strings (`"50units"`, `"two"`, `"N/A"`)
- negative stock values
- missing required fields
- invalid timestamp formats
- duplicate inventory IDs

## Target Collection
Collection: `ai_commerce.inventory`

Document contract:
- `inventory_id`
- `product_id`
- `warehouse_id`
- `available_stock`
- `reserved_stock`
- `damaged_stock`
- `reorder_level`
- `last_updated`
- `batch_number`

## Validation Rules
1. Required fields must be present/non-empty: `inventory_id`, `product_id`, `warehouse_id`, `last_updated`
2. `last_updated` must parse to timestamp
3. Duplicate `inventory_id` rows are dropped
4. Null stock fields default to `0`
5. Negative stock fields are coerced to `0`
6. Missing `batch_number` is auto-set: `BATCH-YYYYMMDD-HHMM`

## Rejection Codes
- `missing_inventory_id`
- `missing_product_id`
- `missing_warehouse_id`
- `missing_last_updated`
- `invalid_last_updated_format`

## Artifact Outputs
- Invalid rows: `data-engineering/inventory_pipeline/logs/invalid_records_<run_id>.json`
- Execution summary: `data-engineering/inventory_pipeline/logs/execution_log_<run_id>.json`
