from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MarketSignal:
    source: str
    summary: str
    score: float = 0.0


def analyze_signal(source: str, summary: str, score: float = 0.0) -> MarketSignal:
    return MarketSignal(source=source, summary=summary, score=score)
