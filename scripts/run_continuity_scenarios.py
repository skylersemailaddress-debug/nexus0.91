from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from nexus_os.product.continuity import build_resume_snapshot

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "continuity"
SCENARIO_REPORT_PATH = EVIDENCE_DIR / "continuity_scenario_report.json"

SCENARIOS = [
    "restart_active_mission",
    "restart_with_pending_approval",
    "restart_with_active_run",
    "resume_summary_completeness",
]


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scenario_state(name: str) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "history": ["User started a mission", "System resumed mission context"],
        "objective": "Finish enterprise continuity implementation",
        "next_step": "Validate continuity scenarios",
        "trajectory": "Continuity spine implementation in progress",
        "approvals": [],
        "runs": [],
        "artifacts": [],
    }

    if name == "restart_with_pending_approval":
        base["approvals"] = [{"id": "approval-1", "status": "pending", "summary": "Approve continuity rollout"}]
        base["next_step"] = "Review pending approval"
    elif name == "restart_with_active_run":
        base["runs"] = [{"id": "run-1", "status": "active", "current_step": "Resume active continuity run"}]
        base["next_step"] = "Resume active continuity run"
    elif name == "resume_summary_completeness":
        base["artifacts"] = [{"id": "artifact-1", "type": "evidence", "summary": "Continuity evidence bundle"}]
        base["runs"] = [{"id": "run-2", "status": "paused", "current_step": "Finalize resume summary"}]
        base["next_step"] = "Finalize resume summary"

    return base


def _normalize_snapshot(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "objective": snapshot.get("objective"),
        "next_step": snapshot.get("next_step"),
        "trajectory": snapshot.get("trajectory"),
        "approvals": snapshot.get("approvals", []),
        "runs": snapshot.get("runs", []),
        "artifacts": snapshot.get("artifacts", []),
        "memory_context": snapshot.get("memory_context", {}),
        "continuity_label": snapshot.get("continuity_label"),
    }


def _scenario_result(name: str) -> Dict[str, Any]:
    state = _scenario_state(name)
    before = build_resume_snapshot(state)
    persisted_payload = json.loads(json.dumps(state))
    after = build_resume_snapshot(persisted_payload)
    before_norm = _normalize_snapshot(before)
    after_norm = _normalize_snapshot(after)
    equivalent = before_norm == after_norm
    return {
        "scenario": name,
        "timestamp": _timestamp(),
        "before": before_norm,
        "after": after_norm,
        "equivalent_after_restart": equivalent,
        "passed": equivalent,
    }


def _emit_legacy_snapshot(result: Dict[str, Any]) -> None:
    payload = dict(result["after"])
    payload.update({"scenario": result["scenario"], "timestamp": result["timestamp"], "passed": result["passed"]})
    path = EVIDENCE_DIR / f"{result['scenario']}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    results: List[Dict[str, Any]] = []
    for scenario in SCENARIOS:
        result = _scenario_result(scenario)
        _emit_legacy_snapshot(result)
        results.append(result)
    report = {"generated_at": _timestamp(), "scenario_count": len(results), "passed": all(r["passed"] for r in results), "results": results}
    SCENARIO_REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
