from __future__ import annotations


DECISION_TERMS = {"approve", "approval", "ship", "release", "commit", "merge"}
BUILD_TERMS = {"build", "implement", "create", "write", "wire", "patch", "fix"}
REVIEW_TERMS = {"review", "audit", "check", "inspect", "validate", "proof"}
RECOVER_TERMS = {"error", "fail", "broken", "recover", "restore"}
STRATEGY_TERMS = {"strategy", "market", "opportunity", "direction", "plan"}


def _tokenize(text: str) -> set[str]:
    return {part.strip(".,:;!?()[]{}\"'").lower() for part in text.split() if part.strip()}


def infer_work_state(history: list[str], mission: str = "") -> str:
    text = " ".join(history[-5:] + ([mission] if mission else []))
    tokens = _tokenize(text)

    if tokens & RECOVER_TERMS:
        return "recover"
    if tokens & DECISION_TERMS:
        return "decide"
    if tokens & REVIEW_TERMS:
        return "review"
    if tokens & BUILD_TERMS:
        return "build"
    return "now"


def infer_need_state(history: list[str], mission: str = "") -> str:
    text = " ".join(history[-5:] + ([mission] if mission else []))
    tokens = _tokenize(text)

    if len(history) >= 8:
        return "builder"
    if tokens & DECISION_TERMS:
        return "operator"
    if tokens & STRATEGY_TERMS:
        return "strategic"
    return "focused"


def compute_active_intelligence_line(history: list[str], mission: str = "") -> str:
    if not history and not mission:
        return "Ready to begin."

    work_state = infer_work_state(history, mission)
    if work_state == "decide":
        return "A decision boundary is approaching."
    if work_state == "build":
        return "Momentum is in build mode."
    if work_state == "review":
        return "This looks like a review and proof moment."
    if work_state == "recover":
        return "Recovery focus is active."
    if mission:
        return f"Mission is active: {mission}"
    return f"Continuing: {history[-1]}"


def compute_next_best_move(history: list[str], mission: str = "") -> str:
    if not history and not mission:
        return "Define your mission."

    work_state = infer_work_state(history, mission)
    if work_state == "decide":
        return "Inspect the decision and approve or hold it."
    if work_state == "build":
        return "Continue execution or review the latest build step."
    if work_state == "review":
        return "Inspect proof and validate the current thread."
    if work_state == "recover":
        return "Stabilize the failure path before continuing."
    if mission:
        return "Advance the mission with one concrete next step."
    return "Continue current thread or inspect status."
