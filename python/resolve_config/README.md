# Resolve Layered Configuration

## Problem

Implement `resolve_config(base, environment, overrides, protected_keys)` to combine three configuration layers with explicit deletion and protected-key rules.

## Input

- `base`, `environment`, and `overrides` are dictionaries with non-empty string keys and JSON-compatible values.
- `protected_keys` is a list of unique, non-empty strings.

## Output

Return a new dictionary with keys inserted in lexicographic order. Nested values must be detached from the input values.

## Rules

- Apply layers in this order: `base`, `environment`, then `overrides`.
- A later non-null value replaces an earlier value.
- A `None` value in `environment` or `overrides` deletes that key if it exists.
- A protected key may be defined in `base`, but its presence in either later layer is invalid, including a matching value or `None`.
- Do not mutate the inputs or share nested lists and dictionaries with the output.

## Invalid Input

Raise `ValueError` for non-dictionary layers, invalid dictionary keys, an invalid or duplicate protected-key list, or any attempt to change or delete a protected key.

## Examples

```python
resolve_config(
    {"endpoint": "primary", "retries": 2, "trace": False},
    {"retries": 3, "trace": None},
    {"timeout": 10},
    ["endpoint"],
)
```

returns:

```python
{"endpoint": "primary", "retries": 3, "timeout": 10}
```

## Evaluation Criteria

The tests check layer precedence, explicit-null deletion, protected keys, sorted output, detached nested values, malformed layers and keys, and fixture behavior.

## Baseline

`baselines/incomplete.py` handles ordinary layer precedence. It does not implement explicit-null deletion or protected keys. The baseline discrimination tests demonstrate those two gaps without identifying the baseline as an agent output.

## Run Locally

From the repository root:

```bash
python -m pytest python/resolve_config/test_solution.py python/resolve_config/test_baseline.py
```
