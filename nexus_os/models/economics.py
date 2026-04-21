from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EconomicsRecord:
    revenue: float
    cost: float

    def profit(self) -> float:
        return self.revenue - self.cost
