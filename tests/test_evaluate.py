from pathlib import Path
import subprocess
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from evaluate import evaluate  # noqa: E402


def manifest(challenge_id="example"):
    return {
        "id": challenge_id,
        "working_directory": ".",
        "test_command": ["python", "-m", "pytest"],
    }


def test_evaluate_reports_pass_and_uses_current_python(tmp_path):
    calls = []

    def runner(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, "", "")

    results, passed = evaluate([manifest()], tmp_path, runner)

    assert passed is True
    assert results == [{"challenge_id": "example", "evaluation_status": "pass"}]
    assert calls[0][0][0] == sys.executable
    assert calls[0][1]["cwd"] == tmp_path


def test_evaluate_reports_failure_and_sorts_results(tmp_path):
    def runner(command, **kwargs):
        return subprocess.CompletedProcess(command, 1, "", "failed")

    results, passed = evaluate(
        [manifest("z-last"), manifest("a-first")], tmp_path, runner
    )

    assert passed is False
    assert results == [
        {"challenge_id": "a-first", "evaluation_status": "fail"},
        {"challenge_id": "z-last", "evaluation_status": "fail"},
    ]


def test_evaluate_treats_missing_executable_as_failure(tmp_path):
    def runner(command, **kwargs):
        raise FileNotFoundError(command[0])

    results, passed = evaluate([manifest()], tmp_path, runner)

    assert passed is False
    assert results[0]["evaluation_status"] == "fail"
