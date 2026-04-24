from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "release" / "evidence"
REPORT_PATH = OUT / "final_certification_scenario_report.json"

REQUIRED_REPORTS = [
    "continuity/continuity_validation_report.json",
    "memory/memory_context_integration_report.json",
    "memory/memory_trace_report.json",
    "memory/memory_behavior_report.json",
    "execution/execution_validation_report.json",
    "ui/ui_validation_report.json",
    "readiness/readiness_validation_report.json",
    "release/release_hardening_report.json",
    "observability/observability_validation_report.json",
    "enterprise_gate/enterprise_gate_coverage_report.json",
]


def main() -> int:
    checks = []
    for rel in REQUIRED_REPORTS:
        path = OUT / rel
        checks.append({"path": rel, "exists": path.exists()})
    passed = all(check["exists"] for check in checks)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "checks": checks,
        "note": "Pre-certification verifies required validation report presence before final certification reads them.",
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
