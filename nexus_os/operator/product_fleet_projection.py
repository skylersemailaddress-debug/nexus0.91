from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProductFleetProjection:
    units: int


def project_fleet(units: int) -> ProductFleetProjection:
    return ProductFleetProjection(units=units)
