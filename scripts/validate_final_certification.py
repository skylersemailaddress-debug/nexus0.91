from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence"
REPORT_PATH = EVIDENCE_DIR / "final_certification_report.json"

REQUIRED_GATES = [
    "continuity",
    "memory",
    "execution",
    "ui",
    "readiness",
    "release",
    "security_governance",
    "observability",
    "adaptive_learning",
    "max_power",
    "full_system_wiring",
    "final_configuration",
]


def main() -> int:
    checks = []
    passed = True

    for gate in REQUIRED_GATES:
        report = EVIDENCE_DIR / gate / f"{gate}_validation_report.json"
        if not report.exists():
            checks.append({"name": gate, "passed": False, "details": ["missing"]})
            passed = False
            continue

        data = json.loads(report.read_text())
        ok = data.get("passed") is True
        checks.append({"name": gate, "passed": ok, "details": [] if ok else ["failed"]})
        if not ok:
            passed = False

    result = {
        "passed": passed,
        "certification": "10/10 Final Nexus" if passed else "FAILED",
        "checks": checks,
    }

    REPORT_PATH.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
