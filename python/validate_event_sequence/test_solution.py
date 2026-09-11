import copy
import json
from pathlib import Path

import pytest

from solution import validate_event_sequence


FIXTURES = Path(__file__).parent / "fixtures"


def test_validates_fixture_case():
    case = json.loads((FIXTURES / "valid_events.json").read_text())
    assert validate_event_sequence(case["input"]) == case["expected"]


def test_empty_input():
    assert validate_event_sequence([]) == {"entities": {}, "ordered_event_ids": []}


def test_orders_by_timestamp_then_event_id_and_sorts_entities():
    events = [
        {"event_id": "b-2", "entity_id": "b", "state": "running", "timestamp": 2},
        {"event_id": "b-1", "entity_id": "b", "state": "queued", "timestamp": 1},
        {"event_id": "a-1", "entity_id": "a", "state": "queued", "timestamp": 1},
    ]
    assert validate_event_sequence(events) == {
        "entities": {"a": "queued", "b": "running"},
        "ordered_event_ids": ["a-1", "b-1", "b-2"],
    }


@pytest.mark.parametrize(
    "states",
    [
        ["running"],
        ["queued", "succeeded"],
        ["queued", "running", "queued"],
        ["queued", "cancelled", "running"],
    ],
)
def test_rejects_illegal_transitions(states):
    events = [
        {"event_id": f"e-{index}", "entity_id": "job", "state": state, "timestamp": index}
        for index, state in enumerate(states)
    ]
    with pytest.raises(ValueError):
        validate_event_sequence(events)


def test_rejects_duplicate_event_ids_across_entities():
    with pytest.raises(ValueError):
        validate_event_sequence(
            [
                {"event_id": "same", "entity_id": "a", "state": "queued", "timestamp": 1},
                {"event_id": "same", "entity_id": "b", "state": "queued", "timestamp": 2},
            ]
        )


@pytest.mark.parametrize("events", [None, {}, "events", 3])
def test_rejects_non_list_input(events):
    with pytest.raises(ValueError):
        validate_event_sequence(events)


@pytest.mark.parametrize("event", [None, [], "event", 2])
def test_rejects_malformed_entries(event):
    with pytest.raises(ValueError):
        validate_event_sequence([event])


@pytest.mark.parametrize("missing", ["event_id", "entity_id", "state", "timestamp"])
def test_rejects_missing_fields(missing):
    event = {"event_id": "e1", "entity_id": "job", "state": "queued", "timestamp": 0}
    del event[missing]
    with pytest.raises(ValueError):
        validate_event_sequence([event])


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("event_id", ""),
        ("event_id", 4),
        ("entity_id", "   "),
        ("entity_id", None),
        ("state", "waiting"),
        ("state", None),
        ("timestamp", -1),
        ("timestamp", 1.5),
        ("timestamp", True),
    ],
)
def test_rejects_invalid_field_values(field, value):
    event = {"event_id": "e1", "entity_id": "job", "state": "queued", "timestamp": 0}
    event[field] = value
    with pytest.raises(ValueError):
        validate_event_sequence([event])


def test_does_not_mutate_input():
    events = [{"event_id": " e1 ", "entity_id": " job ", "state": "queued", "timestamp": 0}]
    before = copy.deepcopy(events)
    validate_event_sequence(events)
    assert events == before


def test_invalid_fixture_is_rejected():
    case = json.loads((FIXTURES / "invalid_events.json").read_text())
    with pytest.raises(ValueError):
        validate_event_sequence(case["input"])
