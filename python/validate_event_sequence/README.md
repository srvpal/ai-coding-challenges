# Validate Event State Transitions

## Problem

Implement `validate_event_sequence(events)` to order event records deterministically and validate each entity's state transitions.

## Input

`events` must be a list of dictionaries. Every event must contain:

- `event_id`: a non-empty string, unique across the input
- `entity_id`: a non-empty string
- `state`: one of `queued`, `running`, `succeeded`, `failed`, or `cancelled`
- `timestamp`: a non-negative integer; booleans are rejected

Additional fields are accepted and ignored.

## Output

Return a dictionary containing final entity states and processed event IDs:

```python
{
    "entities": {"entity-id": "final-state"},
    "ordered_event_ids": ["event-id"],
}
```

Entity keys are sorted lexicographically.

## Rules

- Sort events by `(timestamp, event_id)` before validation.
- Trim surrounding whitespace from `event_id` and `entity_id`.
- An entity's first state must be `queued`.
- `queued` may transition to `running` or `cancelled`.
- `running` may transition to `succeeded`, `failed`, or `cancelled`.
- Terminal states cannot transition again.
- Event IDs remain globally unique after trimming.
- Do not mutate the input.

## Invalid Input

Raise `ValueError` for malformed records, missing fields, invalid field values, duplicate event IDs, unknown states, or illegal transitions.

## Examples

```python
validate_event_sequence([
    {"event_id": "job-2", "entity_id": "job", "state": "running", "timestamp": 20},
    {"event_id": "job-1", "entity_id": "job", "state": "queued", "timestamp": 10},
])
```

returns:

```python
{
    "entities": {"job": "running"},
    "ordered_event_ids": ["job-1", "job-2"],
}
```

## Evaluation Criteria

The tests check deterministic ordering, legal and illegal transitions, terminal states, duplicate IDs, malformed and missing fields, invalid values, empty input, fixture behavior, and input immutability.

## Run Locally

From the repository root:

```bash
python -m pytest python/validate_event_sequence/test_solution.py
```
