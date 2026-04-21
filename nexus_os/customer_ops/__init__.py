from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CustomerEvent:
    event_type: str


def process_event(event_type: str) -> CustomerEvent:
    return CustomerEvent(event_type=event_type)
