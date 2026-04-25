from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_ui_truth_script_runs_without_pythonpath() -> None:
    result = _run([sys.executable, "scripts/run_ui_truth_scenarios.py"])
    assert result.returncode == 0, result.stderr or result.stdout


def test_ui_truth_script_runpy_entrypoint_without_pythonpath() -> None:
    command = [
        sys.executable,
        "-c",
        "import runpy; runpy.run_path('scripts/run_ui_truth_scenarios.py', run_name='__main__')",
    ]
    result = _run(command)
    assert result.returncode == 0, result.stderr or result.stdout
