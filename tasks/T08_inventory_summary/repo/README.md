# inventory

Small helpers for normalising and summarising inventory records.

## Modules

- `inventory.stock`: normalise records and add or remove units.
- `inventory.summary`: compute total units, category counts and low stock names.
- `inventory.format`: render records and summaries as text.

An item without a quantity counts as one unit. An item without a category is placed in `general`.

## Tests

```bash
python -m pytest
```
