from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FleetRecord:
    asset_id: str
    status: str
    severity: str
    action: str


def check_status(asset_id: str) -> FleetRecord:
    if "fail" in asset_id:
        return FleetRecord(asset_id, "down", "high", "recover_and_alert")
    return FleetRecord(asset_id, "ok", "low", "none")


__all__ = ["FleetRecord", "check_status"]
