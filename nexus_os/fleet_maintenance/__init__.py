from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FleetRecord:
    asset_id: str
    status: str


def check_status(asset_id: str) -> FleetRecord:
    return FleetRecord(asset_id=asset_id, status="ok")
