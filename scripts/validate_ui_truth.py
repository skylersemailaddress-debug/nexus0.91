from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "ui"
REPORT_PATH = EVIDENCE_DIR / "ui_validation_report.json"

REQUIRED = [
    "hover_edge_reveal_state.json",
    "bottom_command_rail_state.json",
    "pin_anything_persistence.json",
    "adaptive_opening_state_relevance.json",
    "explain_why_integrity.json",
    "keyboard_parity_contract.json",
    "undo_recovery_state.json",
    "no_dashboard_regression.json",
    "ui_validation_report.json",
]

def _details_for(name: str, data: dict[str, Any]) -> list[str]:
    details: list[str] = []
    scenario = name.replace(".json", "")
    if data.get("scenario") != scenario:
        details.append("scenario_mismatch")

    if scenario == "hover_edge_reveal_state":
        zones = data.get("edge_reveal")
        if not isinstance(zones, list) or not zones:
            details.append("missing_edge_reveal")
        else:
            if not all(bool(z.get("keyboard_shortcut")) for z in zones):
                details.append("edge_zone_missing_keyboard_shortcut")

    elif scenario == "bottom_command_rail_state":
        rail = data.get("bottom_command_rail")
        if not isinstance(rail, dict) or not rail:
            details.append("missing_bottom_command_rail")
        elif not rail.get("mode"):
            details.append("missing_command_rail_mode")

    elif scenario == "pin_anything_persistence":
        pinned = data.get("pinned_items")
        if not isinstance(pinned, list):
            details.append("missing_pinned_items")
        elif not all(str(item.get("persistence_key", "")).startswith("nexus:pinned-items:") for item in pinned):
            details.append("invalid_persistence_key")

    elif scenario == "adaptive_opening_state_relevance":
        adaptive = data.get("adaptive_opening")
        if not isinstance(adaptive, list) or not adaptive:
            details.append("missing_adaptive_opening")
        else:
            for group in adaptive:
                if "relevance_score" not in group or not group.get("reason"):
                    details.append("adaptive_opening_missing_relevance_or_reason")
                    break

    elif scenario == "explain_why_integrity":
        entries = data.get("explain_why")
        if not isinstance(entries, list) or not entries:
            details.append("missing_explain_why")
        else:
            for entry in entries:
                if not entry.get("explanation"):
                    details.append("explain_why_missing_explanation")
                    break
                if not isinstance(entry.get("evidence_ids"), list):
                    details.append("explain_why_missing_evidence_ids")
                    break

    elif scenario == "keyboard_parity_contract":
        contract = data.get("keyboard_parity")
        if not isinstance(contract, dict):
            details.append("missing_keyboard_parity")
        elif not contract.get("passed"):
            details.append("keyboard_parity_failed")

    elif scenario == "undo_recovery_state":
        undo = data.get("undo_recovery")
        if not isinstance(undo, dict):
            details.append("missing_undo_recovery")
        else:
            can_undo = bool(undo.get("can_undo"))
            disabled_reason = str(undo.get("disabled_reason", ""))
            if not can_undo and not disabled_reason:
                details.append("undo_state_not_honest")

    elif scenario == "no_dashboard_regression":
        if bool(data.get("dashboard_detected")):
            details.append("dashboard_regression_detected")

    elif scenario == "ui_validation_report":
        checks = data.get("checks")
        if not isinstance(checks, list) or not checks:
            details.append("ui_validation_report_missing_checks")

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
        details = sorted(set(_details_for(name, data)))
        results.append({"name": name, "passed": not details, "details": details})
    report = {"passed": all(r["passed"] for r in results), "checks": results}
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
