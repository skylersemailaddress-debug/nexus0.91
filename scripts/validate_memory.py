from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "memory"
REPORT_PATH = EVIDENCE_DIR / "memory_gate_report.json"

REQUIRED_REPORTS = {
    "memory_context_integration": EVIDENCE_DIR / "memory_context_integration_report.json",
    "memory_trace": EVIDENCE_DIR / "memory_trace_report.json",
    "memory_behavior": EVIDENCE_DIR / "memory_behavior_report.json",
}


def _passed(data: dict[str, Any]) -> bool:
    if data.get("passed") is not True:
        return False
    checks = data.get("checks")
    if checks is not None:
        if not isinstance(checks, list) or not checks:
            return False
        return all(isinstance(check, dict) and check.get("passed") is True for check in checks)
    return True


def _validate(name: str, path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"name": name, "passed": False, "details": ["missing_report"]}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"name": name, "passed": False, "details": ["invalid_json"]}
    details: list[str] = []
    if not _passed(data):
        details.append("report_not_passed")
    return {"name": name, "passed": not details, "details": details}


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    checks = [_validate(name, path) for name, path in REQUIRED_REPORTS.items()]
    report = {"passed": all(check["passed"] for check in checks), "checks": checks}
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
