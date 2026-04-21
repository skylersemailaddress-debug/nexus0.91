from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProductRecord:
    product_id: str
    name: str
    category: str = "general"
    status: str = "active"
