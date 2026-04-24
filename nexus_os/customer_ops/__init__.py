from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CustomerEvent:
    event_type: str
    severity: str
    churn_risk: str
    next_action: str


def process_event(event_type: str) -> CustomerEvent:
    text = event_type.lower()

    if "churn" in text or "cancel" in text:
        return CustomerEvent(event_type, "high", "high", "trigger_retention_playbook")

    if "complaint" in text or "issue" in text:
        return CustomerEvent(event_type, "medium", "medium", "assign_support")

    return CustomerEvent(event_type, "low", "low", "monitor")


__all__ = ["CustomerEvent", "process_event"]
