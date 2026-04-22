from __future__ import annotations

from .runtime_adapter import get_execution_signal_summary
from .surface_model import ApprovalPrompt


def build_approval_prompt(history: list[str]) -> ApprovalPrompt | None:
    if not history:
        return None

    last = history[-1].lower()

    if "release" in last or "ship" in last or "approve" in last:
        signals = get_execution_signal_summary()

        consequences = []

        if signals["truth_gate"] != "available":
            consequences.append("truth gate is not available")
        if signals["ten_ten_gate"] != "available":
            consequences.append("10/10 gate is not available")
        if signals["release_manifest"] != "present":
            consequences.append("release manifest is not generated")

        if consequences:
            summary = (
                "Approval will proceed but: "
                + ", ".join(consequences)
            )
        else:
            summary = "All release conditions appear satisfied."

        return ApprovalPrompt(
            title="Approval Required",
            summary=summary,
            action_label="approve",
        )

    return None
