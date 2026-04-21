from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PortfolioProjection:
    expected_return: float


def project_portfolio(return_rate: float) -> PortfolioProjection:
    return PortfolioProjection(expected_return=return_rate)
