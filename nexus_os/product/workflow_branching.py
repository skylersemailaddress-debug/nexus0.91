from __future__ import annotations


def should_continue(status: str) -> bool:
    return status == "pass"


def branch_on_failure(step: str) -> str:
    return f"handle failure of {step}"
