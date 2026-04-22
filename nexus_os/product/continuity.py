from __future__ import annotations


def infer_continuity_label(history: list[str]) -> str:
    if not history:
        return "New session"
    return "Resumed thread"
