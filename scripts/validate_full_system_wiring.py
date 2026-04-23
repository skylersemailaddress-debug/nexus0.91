from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "full_system_wiring"
REPORT_PATH = EVIDENCE_DIR / "full_system_wiring_validation_report.json"

REQUIRED = [
    "continuity_memory_execution_handoff.json",
    "execution_approval_ui_observability_consistency.json",
    "readiness_to_action_to_evidence.json",
    "operator_intervention_recovery_consistency.json",
    "full_restart_cross_system_consistency.json",
]


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for name in REQUIRED:
        path = EVIDENCE_DIR / name
        if not path.exists():
            results.append({"name": name, "passed": False, "details": ["missing"]})
            continue

        data = json.loads(path.read_text(encoding="utf-8"))
        passed = (
            data.get("passed") is True
            and data.get("flow")
            and data.get("consistency")
            and data.get("reasoning")
        )
        results.append({"name": name, "passed": bool(passed), "details": [] if passed else ["invalid"]})

    report = {
        "passed": all(r["passed"] for r in results),
        "checks": results,
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
