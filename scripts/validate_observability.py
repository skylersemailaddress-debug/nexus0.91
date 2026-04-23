from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "observability"
REPORT_PATH = EVIDENCE_DIR / "observability_validation_report.json"

REQUIRED = [
    "mission_state_transition_reconstruction.json",
    "failed_run_diagnosis.json",
    "approval_policy_trace_reconstruction.json",
    "memory_influence_trace_inspection.json",
    "readiness_ranking_reason_reconstruction.json",
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
            and data.get("trace")
            and data.get("reasoning")
            and data.get("reconstruction")
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
