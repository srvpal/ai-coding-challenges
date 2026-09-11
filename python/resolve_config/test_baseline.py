import importlib.util
from pathlib import Path


def load_baseline():
    path = Path(__file__).parent / "baselines" / "incomplete.py"
    spec = importlib.util.spec_from_file_location("resolve_config_baseline", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.resolve_config


def test_baseline_is_discriminated_by_explicit_null_case():
    baseline = load_baseline()
    result = baseline({"keep": 1, "remove": 2}, {"remove": None}, {}, [])
    assert result != {"keep": 1}


def test_baseline_is_discriminated_by_protected_key_case():
    baseline = load_baseline()
    result = baseline({"token": "fixed"}, {"token": "changed"}, {}, ["token"])
    assert result == {"token": "changed"}
