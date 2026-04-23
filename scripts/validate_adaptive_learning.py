from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "adaptive_learning"
REPORT_PATH = EVIDENCE_DIR / "adaptive_learning_validation_report.json"

REQUIRED = [
    "repeated_correction_improves_next_step.json",
    "repeated_failure_strategy_adjustment.json",
    "stale_pattern_decay.json",
    "operator_correction_resets_bad_adaptation.json",
    "bounded_under_noisy_signals.json",
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
            and data.get("signal")
            and data.get("adaptation")
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
