"""Run every challenge's declared tests and emit deterministic JSON results."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any, Callable

from validate_manifests import ROOT, load_manifests


Runner = Callable[..., subprocess.CompletedProcess[str]]


def _resolved_command(command: list[str]) -> list[str]:
    resolved = list(command)
    if resolved[0] == "python":
        resolved[0] = sys.executable
    elif resolved[0] == "npm":
        executable = shutil.which("npm") or shutil.which("npm.cmd")
        if not executable and sys.platform == "win32":
            executable = next(
                (
                    str(Path(directory) / "npm.cmd")
                    for directory in os.environ.get("PATH", "").split(os.pathsep)
                    if (Path(directory) / "npm.cmd").is_file()
                ),
                None,
            )
        if executable:
            if sys.platform == "win32" and executable.lower().endswith(".cmd"):
                resolved = [
                    os.environ.get("COMSPEC", "cmd.exe"),
                    "/d",
                    "/s",
                    "/c",
                    executable,
                    *resolved[1:],
                ]
            else:
                resolved[0] = executable
    return resolved


def evaluate(
    manifests: list[dict[str, Any]],
    root: Path = ROOT,
    runner: Runner = subprocess.run,
) -> tuple[list[dict[str, Any]], bool]:
    results = []
    all_passed = True
    for manifest in sorted(manifests, key=lambda item: item["id"]):
        try:
            completed = runner(
                _resolved_command(manifest["test_command"]),
                cwd=root / manifest["working_directory"],
                capture_output=True,
                text=True,
                check=False,
            )
            passed = completed.returncode == 0
        except OSError:
            passed = False
        results.append(
            {
                "challenge_id": manifest["id"],
                "evaluation_status": "pass" if passed else "fail",
            }
        )
        all_passed = all_passed and passed
    return results, all_passed


def main() -> int:
    try:
        manifests = load_manifests()
        results, passed = evaluate(manifests)
    except ValueError as error:
        print(json.dumps({"error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps({"results": results}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
