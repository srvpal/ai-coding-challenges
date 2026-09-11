import json
from pathlib import Path
import sys

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from validate_manifests import load_manifests, validate_manifest  # noqa: E402


def write_manifest(root, challenge_id="sample"):
    challenge = root / "python" / challenge_id
    fixture = challenge / "fixtures" / "case.json"
    fixture.parent.mkdir(parents=True)
    fixture.write_text("{}", encoding="utf-8")
    (challenge / "solution.py").write_text("", encoding="utf-8")
    data = {
        "id": challenge_id,
        "title": "Sample",
        "language": "python",
        "entry_point": f"python/{challenge_id}/solution.py",
        "working_directory": f"python/{challenge_id}",
        "test_command": ["python", "-m", "pytest"],
        "fixtures": [f"python/{challenge_id}/fixtures/case.json"],
        "evaluation_criteria": ["checks behavior"],
        "deterministic_behavior": ["stable output"],
    }
    path = challenge / "manifest.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path, data


def test_valid_manifest_and_sorted_discovery(tmp_path):
    _, second = write_manifest(tmp_path, "zeta")
    _, first = write_manifest(tmp_path, "alpha")

    assert validate_manifest(tmp_path / "python/alpha/manifest.json", tmp_path) == first
    assert load_manifests(tmp_path) == [first, second]


def test_rejects_missing_referenced_file(tmp_path):
    path, data = write_manifest(tmp_path)
    data["fixtures"] = ["missing.json"]
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="fixture does not exist"):
        validate_manifest(path, tmp_path)


def test_rejects_duplicate_ids(tmp_path):
    path, _ = write_manifest(tmp_path, "one")
    other, data = write_manifest(tmp_path, "two")
    data["id"] = "one"
    other.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="ids must be unique"):
        load_manifests(tmp_path)
