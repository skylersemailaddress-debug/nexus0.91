from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EconomicSnapshot:
    revenue: float
    cost: float


def compute_profit(revenue: float, cost: float) -> EconomicSnapshot:
    return EconomicSnapshot(revenue=revenue, cost=cost)
