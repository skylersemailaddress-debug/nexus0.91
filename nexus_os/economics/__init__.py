from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EconomicSnapshot:
    revenue: float
    cost: float
    profit: float
    margin: float
    burn_rate: float
    payback_period: float
    viability: str
    risk_level: str


def _clamp(v: float) -> float:
    return max(0.0, v)


def compute_economics(revenue: float, cost: float) -> EconomicSnapshot:
    revenue = _clamp(revenue)
    cost = _clamp(cost)

    profit = revenue - cost
    margin = profit / revenue if revenue > 0 else 0.0

    burn = cost - revenue if cost > revenue else 0.0

    if revenue > 0:
        payback = cost / revenue
    else:
        payback = float("inf")

    # viability classification
    if profit > 0 and margin >= 0.4:
        viability = "strong"
    elif profit > 0:
        viability = "viable"
    elif burn > 0 and payback < 2:
        viability = "recoverable"
    else:
        viability = "unviable"

    # risk classification
    if margin < 0 or burn > revenue:
        risk = "high"
    elif margin < 0.2:
        risk = "medium"
    else:
        risk = "low"

    return EconomicSnapshot(
        revenue=revenue,
        cost=cost,
        profit=round(profit, 2),
        margin=round(margin, 3),
        burn_rate=round(burn, 2),
        payback_period=round(payback, 2) if payback != float("inf") else float("inf"),
        viability=viability,
        risk_level=risk,
    )


__all__ = ["EconomicSnapshot", "compute_economics"]
