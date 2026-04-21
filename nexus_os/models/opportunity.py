from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OpportunityRecord:
    opportunity_id: str
    description: str
    priority: int = 0
