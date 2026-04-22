from __future__ import annotations

from .surface_model import CapabilityCard


def build_governance_card() -> CapabilityCard:
    return CapabilityCard(
        kind="governance",
        title="Governance",
        summary="Canonical truth gates and validation surfaces are available.",
    )


def build_economics_card() -> CapabilityCard:
    return CapabilityCard(
        kind="economics",
        title="Economics",
        summary="Economics modeling and projection surfaces are available.",
    )


def build_projection_card() -> CapabilityCard:
    return CapabilityCard(
        kind="projection",
        title="Operator Projection",
        summary="Portfolio, market, fleet, and economics projections are available.",
    )
