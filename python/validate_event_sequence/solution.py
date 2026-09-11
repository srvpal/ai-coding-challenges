"""Reference implementation for the validate-event-sequence challenge."""

from __future__ import annotations

from typing import Any


ALLOWED_TRANSITIONS = {
    None: {"queued"},
    "queued": {"running", "cancelled"},
    "running": {"succeeded", "failed", "cancelled"},
    "succeeded": set(),
    "failed": set(),
    "cancelled": set(),
}


def validate_event_sequence(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate state transitions after deterministic chronological ordering."""
    if not isinstance(events, list):
        raise ValueError("events must be a list")

    normalized = []
    seen_event_ids = set()
    required = {"event_id", "entity_id", "state", "timestamp"}

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError(f"event {index} must be a dictionary")
        if required - event.keys():
            raise ValueError(f"event {index} is missing required fields")

        event_id = event["event_id"]
        entity_id = event["entity_id"]
        state = event["state"]
        timestamp = event["timestamp"]
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError(f"event {index} has an invalid event_id")
        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError(f"event {index} has an invalid entity_id")
        if not isinstance(state, str) or state not in ALLOWED_TRANSITIONS:
            raise ValueError(f"event {index} has an invalid state")
        if isinstance(timestamp, bool) or not isinstance(timestamp, int) or timestamp < 0:
            raise ValueError(f"event {index} has an invalid timestamp")

        event_id = event_id.strip()
        entity_id = entity_id.strip()
        if event_id in seen_event_ids:
            raise ValueError(f"duplicate event_id: {event_id}")
        seen_event_ids.add(event_id)
        normalized.append(
            {
                "event_id": event_id,
                "entity_id": entity_id,
                "state": state,
                "timestamp": timestamp,
            }
        )

    ordered = sorted(normalized, key=lambda event: (event["timestamp"], event["event_id"]))
    entity_states: dict[str, str] = {}
    for event in ordered:
        previous = entity_states.get(event["entity_id"])
        if event["state"] not in ALLOWED_TRANSITIONS[previous]:
            raise ValueError(
                f"illegal transition for {event['entity_id']}: {previous} -> {event['state']}"
            )
        entity_states[event["entity_id"]] = event["state"]

    return {
        "entities": {entity_id: entity_states[entity_id] for entity_id in sorted(entity_states)},
        "ordered_event_ids": [event["event_id"] for event in ordered],
    }
