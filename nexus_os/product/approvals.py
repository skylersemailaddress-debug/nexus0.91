from __future__ import annotations

from .surface_model import ApprovalPrompt


def build_approval_prompt(history: list[str]) -> ApprovalPrompt | None:
    if not history:
        return None

    last = history[-1].lower()
    if "release" in last or "ship" in last or "approve" in last:
        return ApprovalPrompt(
            title="Approval Required",
            summary="This thread appears to be approaching a release or approval boundary.",
            action_label="approve",
        )
    return None
