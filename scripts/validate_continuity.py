from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "continuity"
REPORT_PATH = EVIDENCE_DIR / "continuity_validation_report.json"

REQUIRED_EVIDENCE = {
    "restart_active_mission": "restart_active_mission.json",
    "restart_with_pending_approval": "restart_with_pending_approval.json",
    "restart_with_active_run": "restart_with_active_run.json",
    "resume_summary_completeness": "resume_summary_completeness.json",
}

REQUIRED_KEYS = {
    "objective",
    "next_step",
    "trajectory",
    "approvals",
    "runs",
    "artifacts",
    "passed",
}


@dataclass
class CheckResult:
    name: str
    passed: bool
    details: List[str]


def load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence_file(name: str, path: Path) -> CheckResult:
    if not path.exists():
        return CheckResult(name=name, passed=False, details=[f"Missing continuity evidence: {path}"])

    try:
        data = load_json(path)
    except Exception as exc:
        return CheckResult(name=name, passed=False, details=[f"Invalid JSON in {path}: {exc}"])

    details: List[str] = []
    passed = True

    missing_keys = sorted(REQUIRED_KEYS.difference(data.keys()))
    if missing_keys:
        passed = False
        details.extend([f"Missing key in {path.name}: {key}" for key in missing_keys])

    if data.get("passed") is not True:
        passed = False
        details.append(f"Scenario did not pass in {path.name}")

    if not data.get("objective"):
        passed = False
        details.append(f"Empty objective in {path.name}")

    if not data.get("next_step"):
        passed = False
        details.append(f"Empty next_step in {path.name}")

    return CheckResult(name=name, passed=passed, details=details)


def build_report(results: List[CheckResult]) -> Dict[str, object]:
    return {
        "passed": all(result.passed for result in results),
        "checks": [
            {
                "name": result.name,
                "passed": result.passed,
                "details": result.details,
            }
            for result in results
        ],
    }


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    results = [
        validate_evidence_file(name, EVIDENCE_DIR / filename)
        for name, filename in REQUIRED_EVIDENCE.items()
    ]

    report = build_report(results)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
