from __future__ import annotations

import json
from pathlib import Path


def test_next_step_present_in_restart_active_mission() -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "release" / "evidence" / "continuity" / "restart_active_mission.json"

    data = json.loads(target.read_text(encoding="utf-8"))
    assert "next_step" in data
    assert isinstance(data["next_step"], str)
    assert data["next_step"]


def test_next_step_present_in_resume_summary_completeness() -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "release" / "evidence" / "continuity" / "resume_summary_completeness.json"

    data = json.loads(target.read_text(encoding="utf-8"))
    assert "next_step" in data
    assert isinstance(data["next_step"], str)
    assert data["next_step"]
