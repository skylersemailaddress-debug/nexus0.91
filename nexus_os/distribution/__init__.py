from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DistributionPlan:
    name: str


def create_plan(name: str) -> DistributionPlan:
    return DistributionPlan(name=name)
