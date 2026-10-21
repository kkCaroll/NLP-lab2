# recordkit

Small helpers for parsing and grouping simple comma-separated records.

## Modules

- `recordkit.csvio`: split comma-separated fields and parse rows into dictionaries.
- `recordkit.aggregate`: count records per value with case and edge space ignored, and select the most frequent values.
- `recordkit.report`: render counts, record lists and tables as text.

## Tests

```bash
python -m pytest
```
