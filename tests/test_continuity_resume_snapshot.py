from __future__ import annotations

import json
from pathlib import Path


def test_continuity_evidence_files_exist_after_runner_scaffold() -> None:
    root = Path(__file__).resolve().parents[1]
    continuity_dir = root / "docs" / "release" / "evidence" / "continuity"

    expected = [
        continuity_dir / "restart_active_mission.json",
        continuity_dir / "restart_with_pending_approval.json",
        continuity_dir / "restart_with_active_run.json",
        continuity_dir / "resume_summary_completeness.json",
    ]

    missing = [str(path) for path in expected if not path.exists()]
    assert not missing, f"Missing continuity evidence files: {missing}"


def test_continuity_resume_snapshot_shape() -> None:
    root = Path(__file__).resolve().parents[1]
    continuity_dir = root / "docs" / "release" / "evidence" / "continuity"
    target = continuity_dir / "restart_active_mission.json"

    data = json.loads(target.read_text(encoding="utf-8"))

    assert "objective" in data
    assert "next_step" in data
    assert "trajectory" in data
    assert "approvals" in data
    assert "runs" in data
    assert "artifacts" in data
    assert "passed" in data
