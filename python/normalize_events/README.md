# Normalize Event Records

## Problem

Implement `normalize_events(records)` to validate event records and convert them to a deterministic schema without changing the input.

## Input

`records` must be a list of dictionaries. Every dictionary must contain:

- `id`: a string or integer; booleans are rejected
- `label`: a non-empty string after trimming whitespace
- `score`: an integer or float from `0` to `1`, inclusive; booleans are rejected

Additional fields are accepted but are not copied to the output.

## Output

Return a new list sorted lexicographically by the normalized string `id`. Every output dictionary contains exactly:

```python
{"id": str, "label": str, "score": float}
```

## Rules

- Convert each `id` to a string.
- Trim surrounding whitespace from `label`.
- Convert each `score` to a float.
- Sort by the normalized string `id`.
- Return an empty list for empty input.
- Do not mutate the input or retain extra fields.

## Invalid Input

Raise `ValueError` when the input is not a list, a record is not a dictionary, a required field is missing, or a field has an invalid type or value.

## Examples

```python
normalize_events([
    {"id": 20, "label": " relevant ", "score": 1},
    {"id": "10", "label": "incorrect", "score": 0.25},
])
```

returns:

```python
[
    {"id": "10", "label": "incorrect", "score": 0.25},
    {"id": "20", "label": "relevant", "score": 1.0},
]
```

## Evaluation Criteria

The tests check normalization, lexicographic sorting, empty input, score boundaries, rejection of malformed records and invalid field values, removal of extra fields, and input immutability.

## Run Locally

From the repository root:

```bash
python -m pytest python/normalize_events/test_solution.py
```
