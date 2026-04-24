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


def _load(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.exists():
        return None, ["missing_report"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, ["invalid_json"]
    if not isinstance(data, dict):
        return None, ["report_not_object"]
    return data, []


def _checks_pass(data: dict[str, Any]) -> bool:
    if data.get("passed") is not True:
        return False
    checks = data.get("checks")
    if not isinstance(checks, list) or not checks:
        return False
    return all(isinstance(check, dict) and check.get("passed") is True for check in checks)


def _ids(items: Any, key: str = "id") -> list[str]:
    if not isinstance(items, list):
        return []
    return [item.get(key) for item in items if isinstance(item, dict) and isinstance(item.get(key), str)]


def _validate_context(data: dict[str, Any]) -> list[str]:
    details: list[str] = []
    if not _checks_pass(data):
        details.append("checks_not_all_passed")
    without_memory = data.get("without_memory")
    with_memory = data.get("with_memory")
    if not isinstance(without_memory, dict):
        details.append("missing_without_memory_context")
    if not isinstance(with_memory, dict):
        details.append("missing_with_memory_context")
        return details
    if with_memory.get("selected_memories") in (None, []):
        details.append("memory_not_selected")
    if with_memory.get("influence_trace") in (None, []):
        details.append("missing_influence_trace")
    if data.get("behavior_changed") is not True:
        details.append("memory_did_not_change_behavior")
    decision = with_memory.get("decision")
    if not isinstance(decision, dict) or decision.get("memory_influenced") is not True:
        details.append("decision_not_marked_memory_influenced")
    return details


def _validate_trace(data: dict[str, Any]) -> list[str]:
    details: list[str] = []
    if not _checks_pass(data):
        details.append("checks_not_all_passed")
    selected_ids = data.get("selected_ids")
    suppressed_ids = data.get("suppressed_ids")
    filtered_ids = data.get("filtered_ids")
    trace_ids = data.get("trace_ids")
    if selected_ids != ["mem-active"]:
        details.append("active_memory_not_exclusively_selected")
    if not isinstance(suppressed_ids, list) or "mem-duplicate" not in suppressed_ids:
        details.append("duplicate_memory_not_suppressed")
    if not isinstance(filtered_ids, list) or "mem-contradicted" not in filtered_ids:
        details.append("contradicted_memory_not_filtered")
    if trace_ids != selected_ids:
        details.append("trace_does_not_match_selection")
    if isinstance(trace_ids, list) and "mem-contradicted" in trace_ids:
        details.append("contradicted_memory_traced")
    context = data.get("context")
    if not isinstance(context, dict):
        details.append("missing_context_payload")
    else:
        selected_from_context = _ids(context.get("selected_memories"))
        if selected_from_context != selected_ids:
            details.append("context_selection_mismatch")
        trace_from_context = _ids(context.get("influence_trace"), key="memory_id")
        if trace_from_context != selected_ids:
            details.append("context_trace_mismatch")
    return details


def _validate_behavior(data: dict[str, Any]) -> list[str]:
    details: list[str] = []
    if not _checks_pass(data):
        details.append("checks_not_all_passed")
    base = data.get("base")
    variant = data.get("variant")
    if not isinstance(base, dict):
        details.append("missing_base_context")
    if not isinstance(variant, dict):
        details.append("missing_variant_context")
        return details
    if base and base.get("selected_memories") != []:
        details.append("base_selected_memory_unexpectedly")
    if variant.get("selected_memories") in (None, []):
        details.append("variant_memory_not_selected")
    if variant.get("influence_trace") in (None, []):
        details.append("variant_missing_influence_trace")
    if data.get("behavior_changed") is not True:
        details.append("behavior_not_changed")
    decision = variant.get("decision")
    if not isinstance(decision, dict) or decision.get("memory_influenced") is not True:
        details.append("variant_decision_not_memory_influenced")
    return details


def _validate(name: str, path: Path) -> dict[str, Any]:
    data, details = _load(path)
    if data is None:
        return {"name": name, "passed": False, "details": details}
    validators = {
        "memory_context_integration": _validate_context,
        "memory_trace": _validate_trace,
        "memory_behavior": _validate_behavior,
    }
    details.extend(validators[name](data))
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
