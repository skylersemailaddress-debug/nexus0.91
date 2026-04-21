from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Portfolio:
    items: List[str]


def build_portfolio(items: List[str]) -> Portfolio:
    return Portfolio(items=items)
