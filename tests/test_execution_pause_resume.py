from __future__ import annotations

import json
from pathlib import Path


def _load(name: str) -> dict:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "release" / "evidence" / "execution" / f"{name}.json"
    return json.loads(target.read_text(encoding="utf-8"))


def test_pause_resume_job_has_resumed_status() -> None:
    data = _load("pause_resume_job")
    jobs = data.get("jobs", [])
    assert jobs
    assert jobs[0].get("status") == "resumed"


def test_resume_run_has_resumed_or_running_state() -> None:
    data = _load("resume_run")
    status = data.get("run", {}).get("status")
    assert status in {"resumed", "running", "active"}
