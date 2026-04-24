from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence"
REPORT_PATH = EVIDENCE_DIR / "final_certification_report.json"

REQUIRED_REPORTS = {
    "continuity": EVIDENCE_DIR / "continuity" / "continuity_validation_report.json",
    "memory": EVIDENCE_DIR / "memory" / "memory_context_integration_report.json",
    "memory_trace": EVIDENCE_DIR / "memory" / "memory_trace_report.json",
    "memory_behavior": EVIDENCE_DIR / "memory" / "memory_behavior_report.json",
    "execution": EVIDENCE_DIR / "execution" / "execution_validation_report.json",
    "ui_truth": EVIDENCE_DIR / "ui" / "ui_validation_report.json",
    "readiness": EVIDENCE_DIR / "readiness" / "readiness_validation_report.json",
    "release_hardening": EVIDENCE_DIR / "release" / "release_hardening_report.json",
    "observability": EVIDENCE_DIR / "observability" / "observability_validation_report.json",
    "enterprise_gate_coverage": EVIDENCE_DIR / "enterprise_gate" / "enterprise_gate_coverage_report.json",
}


def _report_passed(data: dict[str, Any]) -> bool:
    if data.get("passed") is not True:
        return False
    checks = data.get("checks")
    if checks is not None:
        if not isinstance(checks, list) or not checks:
            return False
        if not all(isinstance(check, dict) and check.get("passed") is True for check in checks):
            return False
    return True


def _validate_report(name: str, path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"name": name, "passed": False, "details": ["missing_report"], "path": str(path.relative_to(ROOT))}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"name": name, "passed": False, "details": ["invalid_json"], "path": str(path.relative_to(ROOT))}
    details = []
    if not _report_passed(data):
        details.append("report_not_passed_or_empty_checks")
    return {"name": name, "passed": not details, "details": details, "path": str(path.relative_to(ROOT))}


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    checks = [_validate_report(name, path) for name, path in REQUIRED_REPORTS.items()]
    passed = all(check["passed"] for check in checks)
    result = {
        "passed": passed,
        "certification": "CERTIFIED_BY_EVIDENCE" if passed else "NO_GO",
        "overclaim_guard": "No 10/10, enterprise-ready, or launch-ready label is authorized unless this report and GitHub CI are green.",
        "checks": checks,
    }
    REPORT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
