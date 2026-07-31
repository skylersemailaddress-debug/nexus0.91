from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List


@dataclass(frozen=True)
class PortfolioItem:
    name: str
    score: float
    priority: str
    effort: str
    risk: str
    urgency: str
    strategic_fit: float
    reasons: list[str] = field(default_factory=list)
    recommended_next_step: str = "validate"


@dataclass(frozen=True)
class Portfolio:
    items: List[str]
    ranked_items: list[PortfolioItem] = field(default_factory=list)
    build_order: list[str] = field(default_factory=list)
    focus: str = "balanced"


VALUE_TERMS = {
    "revenue": 0.16,
    "enterprise": 0.14,
    "customer": 0.1,
    "retention": 0.12,
    "churn": 0.16,
    "automation": 0.1,
    "ai": 0.08,
    "approval": 0.08,
    "compliance": 0.12,
}

URGENCY_TERMS = {"urgent", "blocked", "critical", "deadline", "churn", "security", "broken"}
RISK_TERMS = {"migration", "security", "compliance", "billing", "production", "data", "legal"}
EFFORT_HIGH_TERMS = {"platform", "migration", "enterprise", "integration", "multi-tenant", "security"}
EFFORT_LOW_TERMS = {"copy", "dashboard", "report", "summary", "workflow", "prototype"}


def _norm(text: str) -> str:
    return " ".join(text.lower().split())


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _effort(text: str) -> tuple[str, float, list[str]]:
    high_hits = sorted(term for term in EFFORT_HIGH_TERMS if term in text)
    low_hits = sorted(term for term in EFFORT_LOW_TERMS if term in text)
    if high_hits and len(high_hits) >= len(low_hits):
        return "high", 0.22, [f"high_effort:{','.join(high_hits)}"]
    if low_hits:
        return "low", 0.04, [f"low_effort:{','.join(low_hits)}"]
    return "medium", 0.12, ["medium_effort_default"]


def _risk(text: str) -> tuple[str, float, list[str]]:
    hits = sorted(term for term in RISK_TERMS if term in text)
    if len(hits) >= 2:
        return "high", 0.2, [f"risk_terms:{','.join(hits)}"]
    if hits:
        return "medium", 0.1, [f"risk_terms:{','.join(hits)}"]
    return "low", 0.02, ["low_risk_default"]


def score_item(item: str, focus: str = "balanced") -> PortfolioItem:
    text = _norm(item)
    reasons: list[str] = []
    value = 0.32
    for term, weight in VALUE_TERMS.items():
        if term in text:
            value += weight
            reasons.append(f"value:{term}")
    urgency_hits = sorted(term for term in URGENCY_TERMS if term in text)
    urgency_value = min(0.18, len(urgency_hits) * 0.08)
    if urgency_hits:
        reasons.append(f"urgency:{','.join(urgency_hits)}")
    effort, effort_penalty, effort_reasons = _effort(text)
    risk, risk_penalty, risk_reasons = _risk(text)
    reasons.extend(effort_reasons)
    reasons.extend(risk_reasons)
    strategic_fit = 0.72 if any(term in text for term in ["enterprise", "automation", "ai", "workflow"]) else 0.52
    if focus == "revenue":
        value += 0.08 if "revenue" in text or "customer" in text else 0.0
    if focus == "risk_reduction":
        value += 0.08 if risk != "low" or "compliance" in text else 0.0
    critical_customer_signal = "churn" in text and ("urgent" in text or "customer" in text or "retention" in text)
    critical_customer_bonus = 0.08 if critical_customer_signal else 0.0
    if critical_customer_signal:
        reasons.append("critical_customer_signal:churn")
    score = _clamp(value + urgency_value + critical_customer_bonus + strategic_fit * 0.18 - effort_penalty - risk_penalty)
    if score >= 0.75:
        priority = "P0"
        next_step = "build_blueprint_now"
    elif score >= 0.58:
        priority = "P1"
        next_step = "validate_and_schedule"
    else:
        priority = "P2"
        next_step = "park_or_research"
    urgency = "high" if urgency_value >= 0.12 else "medium" if urgency_value else "low"
    return PortfolioItem(
        name=item,
        score=round(score, 3),
        priority=priority,
        effort=effort,
        risk=risk,
        urgency=urgency,
        strategic_fit=round(strategic_fit, 3),
        reasons=reasons,
        recommended_next_step=next_step,
    )


def build_portfolio(items: List[str], focus: str = "balanced") -> Portfolio:
    ranked = sorted((score_item(item, focus=focus) for item in items), key=lambda x: (x.score, x.strategic_fit), reverse=True)
    return Portfolio(items=items, ranked_items=ranked, build_order=[item.name for item in ranked], focus=focus)


def recommend_next_build(items: Iterable[str], focus: str = "balanced") -> PortfolioItem | None:
    portfolio = build_portfolio(list(items), focus=focus)
    return portfolio.ranked_items[0] if portfolio.ranked_items else None


__all__ = ["Portfolio", "PortfolioItem", "build_portfolio", "score_item", "recommend_next_build"]
