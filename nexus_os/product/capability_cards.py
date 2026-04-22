from __future__ import annotations

from .surface_model import CapabilityCard
from .runtime_adapter import (
    get_release_manifest_state,
    get_ten_ten_gate_state,
    get_truth_gate_state,
)


def build_context_cards(history: list[str]) -> list[CapabilityCard]:
    cards: list[CapabilityCard] = []

    if not history:
        return cards

    last = history[-1].lower()

    if "release" in last or "ship" in last:
        cards.append(
            CapabilityCard(
                kind="governance",
                title="Release Readiness",
                summary=f"Truth gate: {get_truth_gate_state()}, 10/10 gate: {get_ten_ten_gate_state()}, manifest: {get_release_manifest_state()}",
            )
        )

    if "cost" in last or "price" in last or "economics" in last:
        cards.append(
            CapabilityCard(
                kind="economics",
                title="Economics",
                summary="Economic modeling is relevant to this thread.",
            )
        )

    if "market" in last or "strategy" in last:
        cards.append(
            CapabilityCard(
                kind="projection",
                title="Market Projection",
                summary="Strategic/market projection context is active.",
            )
        )

    return cards
