from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "continuity"
REPORT_PATH = EVIDENCE_DIR / "continuity_validation_report.json"
SCENARIO_REPORT_PATH = EVIDENCE_DIR / "continuity_scenario_report.json"

REQUIRED_KEYS = {
    "objective",
    "next_step",
    "trajectory",
    "approvals",
    "runs",
    "artifacts",
}


@dataclass
class CheckResult:
    name: str
    passed: bool
    details: List[str]


def load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_scenario_report(path: Path) -> CheckResult:
    if not path.exists():
        return CheckResult("scenario_report", False, [f"Missing report: {path}"])

    try:
        data = load_json(path)
    except Exception as exc:
        return CheckResult("scenario_report", False, [f"Invalid JSON: {exc}"])

    results = data.get("results", [])
    if not results:
        return CheckResult("scenario_report", False, ["No scenarios present"])

    details: List[str] = []
    passed = True

    for result in results:
        if not result.get("equivalent_after_restart"):
            passed = False
            details.append(f"Scenario failed equivalence: {result.get('scenario')}")

        after = result.get("after", {})
        missing = REQUIRED_KEYS.difference(after.keys())
        if missing:
            passed = False
            details.append(f"Missing keys in scenario {result.get('scenario')}: {sorted(missing)}")

    return CheckResult("scenario_report", passed, details)


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    result = validate_scenario_report(SCENARIO_REPORT_PATH)

    report = {
        "passed": result.passed,
        "checks": [
            {
                "name": result.name,
                "passed": result.passed,
                "details": result.details,
            }
        ],
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
