import copy
import json
from pathlib import Path

import pytest

from solution import resolve_config


FIXTURES = Path(__file__).parent / "fixtures"


def test_resolves_fixture_case():
    case = json.loads((FIXTURES / "valid_case.json").read_text())
    assert resolve_config(
        case["base"], case["environment"], case["overrides"], case["protected_keys"]
    ) == case["expected"]


def test_precedence_and_explicit_null_deletion():
    assert resolve_config(
        {"a": 1, "b": 2, "c": 3},
        {"a": 4, "b": None},
        {"a": 5, "d": 6},
        [],
    ) == {"a": 5, "c": 3, "d": 6}


def test_output_keys_are_sorted():
    result = resolve_config({"z": 1, "a": 2}, {"m": 3}, {}, [])
    assert list(result) == ["a", "m", "z"]


def test_inputs_and_nested_values_are_not_shared_or_mutated():
    base = {"nested": {"enabled": True}}
    environment = {"items": [1, 2]}
    overrides = {}
    protected = ["nested"]
    before = copy.deepcopy((base, environment, overrides, protected))
    result = resolve_config(base, environment, overrides, protected)
    result["nested"]["enabled"] = False
    result["items"].append(3)
    assert (base, environment, overrides, protected) == before


@pytest.mark.parametrize("layer_index", [0, 1, 2])
def test_rejects_non_dictionary_layers(layer_index):
    args = [{}, {}, {}, []]
    args[layer_index] = []
    with pytest.raises(ValueError):
        resolve_config(*args)


@pytest.mark.parametrize("bad_key", ["", 4, None])
def test_rejects_invalid_layer_keys(bad_key):
    with pytest.raises(ValueError):
        resolve_config({bad_key: 1}, {}, {}, [])


@pytest.mark.parametrize("protected", [None, {}, [""], [4], ["token", "token"]])
def test_rejects_invalid_protected_key_lists(protected):
    with pytest.raises(ValueError):
        resolve_config({}, {}, {}, protected)


def test_rejects_protected_key_in_environment_even_if_value_matches():
    with pytest.raises(ValueError):
        resolve_config({"token": "fixed"}, {"token": "fixed"}, {}, ["token"])


def test_rejects_protected_key_deletion_in_overrides():
    case = json.loads((FIXTURES / "invalid_case.json").read_text())
    with pytest.raises(ValueError):
        resolve_config(
            case["base"], case["environment"], case["overrides"], case["protected_keys"]
        )
