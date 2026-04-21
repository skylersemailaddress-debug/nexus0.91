from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PolicyDecision:
    allowed: bool


def evaluate(action: str) -> PolicyDecision:
    return PolicyDecision(allowed=True)
