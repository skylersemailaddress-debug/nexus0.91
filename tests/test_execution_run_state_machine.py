from __future__ import annotations

import json
from pathlib import Path


def _load(name: str) -> dict:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "release" / "evidence" / "execution" / f"{name}.json"
    return json.loads(target.read_text(encoding="utf-8"))


def test_resume_run_contains_run_object() -> None:
    data = _load("resume_run")
    assert "run" in data
    assert isinstance(data["run"], dict)
    assert data["run"].get("id")
    assert data["run"].get("status")


def test_pause_resume_job_contains_jobs_list() -> None:
    data = _load("pause_resume_job")
    assert "jobs" in data
    assert isinstance(data["jobs"], list)
    assert data["jobs"]


def test_fail_repair_revalidate_emits_pass_flag() -> None:
    data = _load("fail_repair_revalidate")
    assert "passed" in data
    assert isinstance(data["passed"], bool)
