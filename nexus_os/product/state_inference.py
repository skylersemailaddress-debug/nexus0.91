from __future__ import annotations


def infer_work_state(history: list[str]) -> str:
    if not history:
        return "now"
    last = history[-1]
    if "build" in last:
        return "build"
    if "decide" in last:
        return "decide"
    if "review" in last:
        return "review"
    if "error" in last or "fail" in last:
        return "recover"
    return "now"


def infer_need_state(history: list[str]) -> str:
    if len(history) > 5:
        return "builder"
    return "strategic"


def compute_active_intelligence_line(history: list[str]) -> str:
    if not history:
        return "Ready to begin."
    return f"Continuing: {history[-1]}"


def compute_next_best_move(history: list[str]) -> str:
    if not history:
        return "Define your mission."
    return "Continue current thread or inspect status."
