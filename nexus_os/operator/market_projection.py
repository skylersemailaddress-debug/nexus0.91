from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MarketProjection:
    growth_rate: float


def project_market(growth_rate: float) -> MarketProjection:
    return MarketProjection(growth_rate=growth_rate)
