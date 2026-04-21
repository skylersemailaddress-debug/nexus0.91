from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class PortfolioRecord:
    portfolio_id: str
    products: List[str]
