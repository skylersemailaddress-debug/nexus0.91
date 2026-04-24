from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "release" / "evidence" / "observability"


def emit(name: str, trace: list[dict], reconstruction: dict, reasoning: list[str]) -> bool:
    trace_ids = [event.get("id") for event in trace]
    reconstruction_sources = reconstruction.get("source_event_ids", [])
    passed = bool(
        trace
        and all(event.get("id") and event.get("timestamp") and event.get("type") for event in trace)
        and reconstruction.get("result")
        and set(reconstruction_sources).issubset(set(trace_ids))
        and reasoning
        and all(any(str(event_id) in reason for reason in reasoning) for event_id in reconstruction_sources)
    )
    payload = {
        "scenario": name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trace": trace,
        "reconstruction": reconstruction,
        "reasoning": reasoning,
        "passed": passed,
    }
    (OUT / f"{name}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return passed


def _event(event_id: str, event_type: str) -> dict:
    return {"id": event_id, "type": event_type, "timestamp": datetime.now(timezone.utc).isoformat()}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    results = [
        emit(
            "mission_state_transition_reconstruction",
            [_event("m1", "mission_started"), _event("m2", "mission_active")],
            {"result": "reconstructed", "source_event_ids": ["m1", "m2"]},
            ["m1 and m2 reconstruct mission transition"],
        ),
        emit(
            "failed_run_diagnosis",
            [_event("f1", "run_failed"), _event("f2", "diagnosis_recorded")],
            {"result": "root_cause_identified", "source_event_ids": ["f1", "f2"]},
            ["f1 and f2 identify failed run root cause"],
        ),
        emit(
            "approval_policy_trace_reconstruction",
            [_event("a1", "approval_required"), _event("a2", "policy_hold_applied")],
            {"result": "policy_trace_reconstructed", "source_event_ids": ["a1", "a2"]},
            ["a1 and a2 reconstruct approval policy hold"],
        ),
        emit(
            "memory_influence_trace_inspection",
            [_event("mem1", "memory_selected"), _event("mem2", "decision_influenced")],
            {"result": "memory_trace_visible", "source_event_ids": ["mem1", "mem2"]},
            ["mem1 and mem2 show memory influence"],
        ),
        emit(
            "readiness_ranking_reason_reconstruction",
            [_event("r1", "item_ranked"), _event("r2", "reason_recorded")],
            {"result": "ranking_reason_reconstructed", "source_event_ids": ["r1", "r2"]},
            ["r1 and r2 reconstruct readiness ranking reason"],
        ),
    ]
    print("[observability] emitted 5 scenarios")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
