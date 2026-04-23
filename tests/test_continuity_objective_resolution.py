from __future__ import annotations

import json
from pathlib import Path


def test_objective_present_in_restart_active_mission() -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "release" / "evidence" / "continuity" / "restart_active_mission.json"

    data = json.loads(target.read_text(encoding="utf-8"))
    assert "objective" in data
    assert isinstance(data["objective"], str)
    assert data["objective"]


def test_objective_present_in_restart_with_active_run() -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "release" / "evidence" / "continuity" / "restart_with_active_run.json"

    data = json.loads(target.read_text(encoding="utf-8"))
    assert "objective" in data
    assert isinstance(data["objective"], str)
    assert data["objective"]
