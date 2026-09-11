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


def test_empty_input_returns_empty_list():
    assert normalize_events([]) == []


@pytest.mark.parametrize("records", [None, {}, "records", 3])
def test_rejects_non_list_input(records):
    with pytest.raises(ValueError):
        normalize_events(records)


@pytest.mark.parametrize("entry", [None, [], "record", 4])
def test_rejects_non_dictionary_entries(entry):
    with pytest.raises(ValueError):
        normalize_events([entry])


@pytest.mark.parametrize("event_id", [True, None, 1.5, [], {}])
def test_rejects_invalid_id_types(event_id):
    with pytest.raises(ValueError):
        normalize_events([{"id": event_id, "label": "valid", "score": 0.5}])


@pytest.mark.parametrize("label", [None, 4, [], "", "   "])
def test_rejects_invalid_labels(label):
    with pytest.raises(ValueError):
        normalize_events([{"id": 1, "label": label, "score": 0.5}])


@pytest.mark.parametrize("score", [None, "0.5", [], -0.01, 1.01, True])
def test_rejects_invalid_scores(score):
    with pytest.raises(ValueError):
        normalize_events([{"id": 1, "label": "valid", "score": score}])


def test_accepts_score_boundaries():
    assert normalize_events(
        [
            {"id": "zero", "label": "low", "score": 0},
            {"id": "one", "label": "high", "score": 1},
        ]
    ) == [
        {"id": "one", "label": "high", "score": 1.0},
        {"id": "zero", "label": "low", "score": 0.0},
    ]


@pytest.mark.parametrize("missing", ["id", "label", "score"])
def test_rejects_each_missing_required_field(missing):
    record = {"id": 1, "label": "valid", "score": 0.5}
    del record[missing]
    with pytest.raises(ValueError):
        normalize_events([record])


def test_discards_extra_fields_and_sorts_by_normalized_id():
    records = [
        {"id": 2, "label": "second", "score": 0.2, "source": "extra"},
        {"id": "10", "label": "first", "score": 0.1, "ignored": True},
    ]
    assert normalize_events(records) == [
        {"id": "10", "label": "first", "score": 0.1},
        {"id": "2", "label": "second", "score": 0.2},
    ]
