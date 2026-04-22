from __future__ import annotations

from .runtime_adapter import (
    get_execution_signal_summary,
    get_gate_execution_summary,
)
from .surface_model import ApprovalPrompt


def build_approval_prompt(history: list[str]) -> ApprovalPrompt | None:
    if not history:
        return None

    last = history[-1].lower()

    if "release" in last or "ship" in last or "approve" in last:
        signals = get_execution_signal_summary()
        gate_results = get_gate_execution_summary()

        issues = []

        if gate_results["truth_gate"] != "pass":
            issues.append("truth gate failing")
        if gate_results["ten_ten_gate"] != "pass":
            issues.append("10/10 gate failing")
        if signals["release_manifest"] != "present":
            issues.append("release manifest missing")

        if issues:
            summary = (
                "Not ready for release: " + ", ".join(issues)
            )
            alternatives = "Options: fix issues, run validation, or hold release"
        else:
            summary = "All gates passing. Release is safe to proceed."
            alternatives = "Options: approve release or re-check validation"

        return ApprovalPrompt(
            title="Approval Required",
            summary=summary + ". " + alternatives,
            action_label="approve",
        )

    return None
