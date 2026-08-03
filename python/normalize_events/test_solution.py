import copy
import pytest
from solution import normalize_events


def test_normalizes_and_sorts_records():
    records = [
        {"id": 20, "label": " relevant ", "score": 1},
        {"id": "10", "label": "incorrect", "score": 0.25},
    ]
    assert normalize_events(records) == [
        {"id": "10", "label": "incorrect", "score": 0.25},
        {"id": "20", "label": "relevant", "score": 1.0},
    ]


def test_does_not_mutate_input():
    records = [{"id": 1, "label": " valid ", "score": 0.5}]
    original = copy.deepcopy(records)
    normalize_events(records)
    assert records == original


@pytest.mark.parametrize(
    "records",
    [
        [{"id": 1, "label": "", "score": 0.5}],
        [{"id": 1, "label": "valid", "score": 1.1}],
        [{"id": 1, "label": "valid", "score": True}],
        [{"label": "valid", "score": 0.5}],
    ],
)
def test_rejects_invalid_records(records):
    with pytest.raises(ValueError):
        normalize_events(records)
