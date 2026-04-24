from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    risk_level: str = "low"
    requires_approval: bool = False
    blocked: bool = False
    audit_required: bool = False
    reasons: list[str] = field(default_factory=list)
    controls: list[str] = field(default_factory=list)


BLOCK_TERMS = {
    "delete production",
    "drop database",
    "disable auth",
    "bypass approval",
    "exfiltrate",
    "leak secret",
    "send password",
    "unsafe deploy",
    "force push main",
}

APPROVAL_TERMS = {
    "deploy",
    "production",
    "billing",
    "payment",
    "customer data",
    "migration",
    "schema change",
    "email customers",
    "delete",
    "rotate key",
}

AUDIT_TERMS = {
    "security",
    "auth",
    "admin",
    "pii",
    "customer data",
    "compliance",
    "billing",
    "production",
}

LOW_RISK_TERMS = {
    "draft",
    "summarize",
    "read",
    "analyze",
    "plan",
    "comment",
    "local test",
}


def _norm(action: str) -> str:
    return " ".join(action.lower().split())


def evaluate(action: str) -> PolicyDecision:
    text = _norm(action)
    if not text:
        return PolicyDecision(
            allowed=False,
            risk_level="unknown",
            blocked=True,
            audit_required=True,
            reasons=["empty_action"],
            controls=["provide_action_before_execution"],
        )

    block_hits = sorted(term for term in BLOCK_TERMS if term in text)
    approval_hits = sorted(term for term in APPROVAL_TERMS if term in text)
    audit_hits = sorted(term for term in AUDIT_TERMS if term in text)
    low_hits = sorted(term for term in LOW_RISK_TERMS if term in text)

    if block_hits:
        return PolicyDecision(
            allowed=False,
            risk_level="critical",
            requires_approval=True,
            blocked=True,
            audit_required=True,
            reasons=[f"blocked_terms:{','.join(block_hits)}"],
            controls=["human_approval_required", "security_review_required", "write_operation_blocked"],
        )

    if approval_hits:
        risk = "high" if audit_hits else "medium"
        return PolicyDecision(
            allowed=False,
            risk_level=risk,
            requires_approval=True,
            blocked=False,
            audit_required=bool(audit_hits),
            reasons=[f"approval_terms:{','.join(approval_hits)}"],
            controls=["human_approval_required", "preflight_plan_required", "rollback_plan_required"],
        )

    if audit_hits:
        return PolicyDecision(
            allowed=True,
            risk_level="medium",
            requires_approval=False,
            blocked=False,
            audit_required=True,
            reasons=[f"audit_terms:{','.join(audit_hits)}"],
            controls=["audit_log_required", "least_privilege_required"],
        )

    risk = "low" if low_hits else "medium"
    return PolicyDecision(
        allowed=True,
        risk_level=risk,
        requires_approval=False,
        blocked=False,
        audit_required=False,
        reasons=["low_risk_action" if low_hits else "unclassified_action_allowed_with_monitoring"],
        controls=["standard_logging"],
    )


def require_approval(action: str) -> bool:
    return evaluate(action).requires_approval


def is_blocked(action: str) -> bool:
    return evaluate(action).blocked


__all__ = ["PolicyDecision", "evaluate", "require_approval", "is_blocked"]
