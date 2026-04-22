from __future__ import annotations

from .runtime_adapter import (
    get_release_manifest_state,
    get_ten_ten_gate_state,
    get_truth_gate_state,
)
from .surface_model import TrustPanel


def build_trust_panel(history: list[str]) -> TrustPanel:
    truth = get_truth_gate_state()
    ten = get_ten_ten_gate_state()
    manifest = get_release_manifest_state()

    if not history:
        return TrustPanel(
            title="Trust",
            lines=[
                "No prior actions to analyze.",
                f"Truth gate: {truth}",
                f"10/10 gate: {ten}",
                f"Manifest: {manifest}",
            ],
        )

    last = history[-1]

    return TrustPanel(
        title="Reasoning + Proof",
        lines=[
            f"Last action: {last}",
            f"Truth gate: {truth}",
            f"10/10 gate: {ten}",
            f"Manifest: {manifest}",
            "Assumption: continuing current thread",
        ],
    )
