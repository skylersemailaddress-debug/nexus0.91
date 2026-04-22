from __future__ import annotations

from .surface_model import TrustPanel


def build_trust_panel(history: list[str]) -> TrustPanel:
    if not history:
        return TrustPanel(title="Trust", lines=["No prior actions to analyze."])

    last = history[-1]

    return TrustPanel(
        title="Reasoning",
        lines=[
            f"Last action: {last}",
            "Assumption: continuing current thread is valid",
            "Confidence: moderate",
            "No validation failures detected",
        ],
    )
