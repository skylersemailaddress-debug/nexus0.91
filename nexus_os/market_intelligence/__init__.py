from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class MarketSignal:
    source: str
    summary: str
    score: float = 0.0
    customer_pains: list[str] = field(default_factory=list)
    urgency: str = "medium"
    competitor_risk: str = "medium"
    opportunity_score: float = 0.0
    confidence: float = 0.0
    recommended_action: str = "investigate"
    evidence: list[str] = field(default_factory=list)


PAIN_TERMS = {
    "slow": "speed",
    "manual": "manual_work",
    "messy": "messy_input",
    "churn": "retention",
    "expensive": "cost",
    "compliance": "compliance",
    "security": "security",
    "enterprise": "enterprise_need",
    "spreadsheet": "spreadsheet_workflow",
    "approval": "approval_bottleneck",
}

URGENCY_TERMS = {"urgent", "blocked", "critical", "churn", "deadline", "broken", "security"}
COMPETITOR_TERMS = {"competitor", "alternative", "vendor", "copy", "pricing", "commoditized"}


def _norm(text: str) -> str:
    return " ".join(text.lower().split())


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def analyze_signal(source: str, summary: str, score: float = 0.0) -> MarketSignal:
    text = _norm(f"{source} {summary}")
    pains = [label for term, label in PAIN_TERMS.items() if term in text]
    urgency_hits = sorted(term for term in URGENCY_TERMS if term in text)
    competitor_hits = sorted(term for term in COMPETITOR_TERMS if term in text)
    enterprise_bonus = 0.15 if "enterprise" in text else 0.0
    pain_score = min(len(set(pains)) * 0.12, 0.48)
    urgency_score = min(len(urgency_hits) * 0.12, 0.36)
    competitor_penalty = min(len(competitor_hits) * 0.07, 0.21)
    normalized_input_score = _clamp(score / 100 if score > 1 else score)
    opportunity_score = _clamp(0.25 + normalized_input_score * 0.25 + pain_score + urgency_score + enterprise_bonus - competitor_penalty)
    confidence = _clamp(0.35 + min(len(summary.split()) / 80, 0.25) + len(set(pains)) * 0.04 + normalized_input_score * 0.2)
    urgency = "high" if urgency_score >= 0.24 or "churn" in text else "medium" if urgency_score else "low"
    competitor_risk = "high" if len(competitor_hits) >= 2 else "medium" if competitor_hits else "low"
    if opportunity_score >= 0.72 and confidence >= 0.55:
        action = "prioritize_discovery_and_blueprint"
    elif opportunity_score >= 0.5:
        action = "run_customer_validation"
    else:
        action = "monitor_and_collect_more_signal"
    evidence = []
    if pains:
        evidence.append(f"pain_terms:{','.join(sorted(set(pains)))}")
    if urgency_hits:
        evidence.append(f"urgency_terms:{','.join(urgency_hits)}")
    if competitor_hits:
        evidence.append(f"competitor_terms:{','.join(competitor_hits)}")
    return MarketSignal(
        source=source,
        summary=summary,
        score=score,
        customer_pains=sorted(set(pains)),
        urgency=urgency,
        competitor_risk=competitor_risk,
        opportunity_score=round(opportunity_score, 3),
        confidence=round(confidence, 3),
        recommended_action=action,
        evidence=evidence,
    )


def rank_market_signals(signals: Iterable[MarketSignal]) -> list[MarketSignal]:
    return sorted(signals, key=lambda s: (s.opportunity_score, s.confidence), reverse=True)


__all__ = ["MarketSignal", "analyze_signal", "rank_market_signals"]
