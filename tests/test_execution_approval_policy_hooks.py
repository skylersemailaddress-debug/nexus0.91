from __future__ import annotations

import json
from pathlib import Path


def _load(name: str) -> dict:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "release" / "evidence" / "execution" / f"{name}.json"
    return json.loads(target.read_text(encoding="utf-8"))


def test_approval_blocked_execution_marks_run_blocked() -> None:
    data = _load("approval_blocked_execution")
    assert data.get("run", {}).get("status") == "blocked"


def test_approval_blocked_execution_contains_pending_approval() -> None:
    data = _load("approval_blocked_execution")
    approvals = data.get("run", {}).get("approvals", [])
    assert approvals
    assert approvals[0].get("status") == "pending"


def test_approval_blocked_execution_marks_job_waiting_and_blocked() -> None:
    data = _load("approval_blocked_execution")
    jobs = data.get("jobs", [])
    assert jobs
    assert jobs[0].get("status") == "waiting"
    assert jobs[0].get("blocked_by_approval") is True
