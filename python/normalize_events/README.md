# Normalize Event Records

Implement `normalize_events(records)`.

Each input record must contain:

- `id`: string or integer
- `label`: non-empty string
- `score`: numeric value from 0 to 1

Return a new list sorted by normalized string `id`. Each output record must have exactly:

```python
{"id": str, "label": str, "score": float}
```

Whitespace surrounding `label` must be removed. Booleans are not accepted as numeric scores. Raise `ValueError` for invalid records. Do not mutate the input.
