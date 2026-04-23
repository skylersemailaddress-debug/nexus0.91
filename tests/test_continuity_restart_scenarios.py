from __future__ import annotations

import json
from pathlib import Path


def _load(name: str) -> dict:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "release" / "evidence" / "continuity" / f"{name}.json"
    return json.loads(target.read_text(encoding="utf-8"))


def test_restart_with_pending_approval_contains_approvals_list() -> None:
    data = _load("restart_with_pending_approval")
    assert "approvals" in data
    assert isinstance(data["approvals"], list)


def test_restart_with_active_run_contains_runs_list() -> None:
    data = _load("restart_with_active_run")
    assert "runs" in data
    assert isinstance(data["runs"], list)


def test_resume_summary_completeness_contains_artifacts_list() -> None:
    data = _load("resume_summary_completeness")
    assert "artifacts" in data
    assert isinstance(data["artifacts"], list)


def test_all_restart_scenarios_emit_pass_flag() -> None:
    for name in [
        "restart_active_mission",
        "restart_with_pending_approval",
        "restart_with_active_run",
        "resume_summary_completeness",
    ]:
        data = _load(name)
        assert "passed" in data
        assert isinstance(data["passed"], bool)
