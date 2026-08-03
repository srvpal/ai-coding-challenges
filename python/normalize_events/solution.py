"""Reference implementation for the normalize-events challenge."""

from __future__ import annotations
from typing import Any


def normalize_events(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate, normalize, and sort event records without mutating the input."""
    if not isinstance(records, list):
        raise ValueError("records must be a list")

    normalized: list[dict[str, Any]] = []

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"record {index} must be a dictionary")

        missing = {"id", "label", "score"} - record.keys()
        if missing:
            raise ValueError(f"record {index} is missing: {sorted(missing)}")

        event_id = record["id"]
        if isinstance(event_id, bool) or not isinstance(event_id, (str, int)):
            raise ValueError(f"record {index} has an invalid id")

        label = record["label"]
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"record {index} has an invalid label")

        score = record["score"]
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"record {index} has an invalid score")
        if not 0 <= float(score) <= 1:
            raise ValueError(f"record {index} score must be between 0 and 1")

        normalized.append(
            {"id": str(event_id), "label": label.strip(), "score": float(score)}
        )

    return sorted(normalized, key=lambda item: item["id"])
