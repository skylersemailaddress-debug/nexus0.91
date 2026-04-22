from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "release" / "evidence" / "behavioral_runtime" / "behavioral_runtime_report.json"

REQUIRED_FILES = {
    "behavioral_gate": ROOT / "scripts" / "validate_behavioral_ten_ten_gate.py",
    "ui_gate": ROOT / "scripts" / "validate_ui_master_truth.py",
    "behavioral_work_plan": ROOT / "docs" / "release" / "BEHAVIORAL_TEN_TEN_WORK_PLAN.md",
    "ui_master_truth": ROOT / "docs" / "ui" / "NEXUS_UI_MASTER_TRUTH.md",
}

SCENARIO_MARKERS = {
    "continuity_runtime": [
        "durable message append",
        "restart + resume correctness",
        "objective and next step resolution",
    ],
    "memory_runtime": [
        "memory influences output",
        "memory relevance ranking works",
        "bad memory is filtered",
    ],
    "execution_runtime": [
        "jobs persist across time",
        "jobs resume after interruption",
        "retries and repair loops work",
    ],
    "ui_runtime": [
        "ui reflects real system state",
        "no decorative panels",
        "approvals and jobs are real",
    ],
}

EVIDENCE_FILES = {
    "ui_truth": ROOT / "docs" / "release" / "evidence" / "ui" / "ui_master_truth_report.json",
    "behavioral_gate": ROOT / "docs" / "release" / "evidence" / "behavioral_gate" / "behavioral_ten_ten_report.json",
}


def read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    result: dict[str, object] = {"ok": True, "checks": {}, "errors": [], "notes": []}

    def fail(message: str) -> None:
        result["ok"] = False
        errors = result["errors"]
        assert isinstance(errors, list)
        errors.append(message)

    required_checks: dict[str, object] = {}
    for key, path in REQUIRED_FILES.items():
        exists = path.exists()
        required_checks[key] = {"ok": exists, "path": str(path)}
        if not exists:
            fail(f"Missing required runtime validation dependency: {path}")
    result["checks"]["required_files"] = required_checks

    corpus = "\n\n".join(read_if_exists(path) for path in REQUIRED_FILES.values())
    scenario_checks: dict[str, object] = {}
    for category, markers in SCENARIO_MARKERS.items():
        missing = [marker for marker in markers if marker.lower() not in corpus.lower()]
        scenario_checks[category] = {"ok": not missing, "missing_markers": missing}
        if missing:
            fail(f"Missing runtime scenario markers for {category}: {missing}")
    result["checks"]["scenario_markers"] = scenario_checks

    evidence_checks: dict[str, object] = {}
    for key, path in EVIDENCE_FILES.items():
        exists = path.exists()
        evidence_checks[key] = {"ok": exists, "path": str(path)}
        if not exists:
            fail(f"Missing expected evidence file: {path}")
    result["checks"]["evidence_files"] = evidence_checks

    notes = result["notes"]
    assert isinstance(notes, list)
    notes.append(
        "This validator enforces the runtime-proof contract shape now and is designed to be upgraded into live scenario execution as continuity, memory, execution, and UI runtime endpoints stabilize."
    )

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if bool(result["ok"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
