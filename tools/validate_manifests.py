"""Validate challenge manifests and their referenced repository files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = {
    "id",
    "title",
    "language",
    "entry_point",
    "working_directory",
    "test_command",
    "fixtures",
    "evaluation_criteria",
    "deterministic_behavior",
}
LANGUAGES = {"python", "javascript"}


def discover_manifests(root: Path = ROOT) -> list[Path]:
    return sorted(
        path for path in root.glob("**/manifest.json") if "node_modules" not in path.parts
    )


def _nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    )


def validate_manifest(path: Path, root: Path = ROOT) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{path}: unreadable JSON: {error}") from error

    missing = REQUIRED_FIELDS - data.keys() if isinstance(data, dict) else REQUIRED_FIELDS
    if not isinstance(data, dict) or missing:
        raise ValueError(f"{path}: missing fields: {', '.join(sorted(missing))}")
    for field in ("id", "title", "entry_point", "working_directory"):
        if not isinstance(data[field], str) or not data[field].strip():
            raise ValueError(f"{path}: {field} must be a non-empty string")
    if data["language"] not in LANGUAGES:
        raise ValueError(f"{path}: unsupported language: {data['language']!r}")
    for field in ("test_command", "fixtures", "evaluation_criteria", "deterministic_behavior"):
        if not _nonempty_strings(data[field]):
            raise ValueError(f"{path}: {field} must be a non-empty string list")

    for field in ("entry_point", "working_directory"):
        target = (root / data[field]).resolve()
        if not target.is_relative_to(root.resolve()) or not target.exists():
            raise ValueError(f"{path}: {field} does not exist inside the repository")
    for fixture in data["fixtures"]:
        target = (root / fixture).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            raise ValueError(f"{path}: fixture does not exist: {fixture}")
    return data


def load_manifests(root: Path = ROOT) -> list[dict[str, Any]]:
    paths = discover_manifests(root)
    if not paths:
        raise ValueError("no challenge manifests found")
    manifests = [validate_manifest(path, root) for path in paths]
    ids = [manifest["id"] for manifest in manifests]
    if len(ids) != len(set(ids)):
        raise ValueError("challenge manifest ids must be unique")
    return sorted(manifests, key=lambda manifest: manifest["id"])


def main() -> int:
    try:
        manifests = load_manifests()
    except ValueError as error:
        print(error)
        return 1
    print(f"validated {len(manifests)} challenge manifests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
