from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EconomicsProjection:
    profit: float


def project_economics(revenue: float, cost: float) -> EconomicsProjection:
    return EconomicsProjection(profit=revenue - cost)
