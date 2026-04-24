from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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


def _validate(name: str, data: dict[str, Any]) -> list[str]:
    details: list[str] = []
    trace = data.get("trace")
    reconstruction = data.get("reconstruction")
    reasoning = data.get("reasoning")

    if not isinstance(trace, list) or not trace:
        details.append("missing_trace")
        trace = []
    else:
        for i, event in enumerate(trace):
            if not isinstance(event, dict):
                details.append(f"invalid_event_{i}")
                continue
            if not event.get("id"):
                details.append(f"missing_event_id_{i}")
            if not event.get("type"):
                details.append(f"missing_event_type_{i}")
            if not event.get("timestamp"):
                details.append(f"missing_event_timestamp_{i}")

    if not isinstance(reconstruction, dict) or not reconstruction.get("result"):
        details.append("missing_reconstruction")
    else:
        sources = reconstruction.get("source_event_ids")
        if not isinstance(sources, list) or not sources:
            details.append("missing_source_event_ids")
        else:
            trace_ids = {event.get("id") for event in trace if isinstance(event, dict)}
            for sid in sources:
                if sid not in trace_ids:
                    details.append(f"source_not_in_trace:{sid}")

    if not isinstance(reasoning, list) or not reasoning:
        details.append("missing_reasoning")
    else:
        reason_text = " ".join(reasoning)
        if isinstance(reconstruction, dict):
            for sid in reconstruction.get("source_event_ids", []):
                if sid not in reason_text:
                    details.append(f"reasoning_missing_reference:{sid}")

    return details


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for name in REQUIRED:
        path = EVIDENCE_DIR / name
        if not path.exists():
            results.append({"name": name, "passed": False, "details": ["missing"]})
            continue

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            results.append({"name": name, "passed": False, "details": ["invalid_json"]})
            continue

        details = sorted(set(_validate(name, data)))
        results.append({"name": name, "passed": not details, "details": details})

    report = {"passed": all(r["passed"] for r in results), "checks": results}
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
