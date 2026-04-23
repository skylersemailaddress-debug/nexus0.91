from __future__ import annotations

import re
from typing import Any


STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "for", "with", "in", "on", "at", "by", "is", "are", "be",
    "this", "that", "it", "as", "from", "into", "must",
}

HIGH_SIGNAL_TERMS = {
    "enterprise", "runtime", "persistence", "trace", "replay", "memory", "execution", "approval", "release",
}


def _terms(text: str) -> set[str]:
    raw = re.findall(r"[A-Za-z0-9_\-]+", text.lower())
    return {token for token in raw if token and token not in STOPWORDS}


def _score_memory(query_terms: set[str], memory: dict[str, Any]) -> tuple[float, str]:
    content = str(memory.get("content", ""))
    content_terms = _terms(content)
    overlap = query_terms.intersection(content_terms)
    score = float(len(overlap))

    exact_bonus = 0.0
    query_phrase = " ".join(sorted(query_terms))
    if query_phrase and query_phrase in " ".join(sorted(content_terms)):
        exact_bonus = 2.0

    high_signal_bonus = float(len(overlap.intersection(HIGH_SIGNAL_TERMS))) * 0.5
    penalty = 1.0 if len(overlap) == 0 else 0.0

    final = score + exact_bonus + high_signal_bonus - penalty
    reason = "high_relevance" if final > 1.5 else ("term_overlap" if final > 0 else "low_relevance")
    return final, reason


def build_context(*, query: str, memories: list[dict[str, Any]]) -> dict[str, Any]:
    query_terms = _terms(query)

    selected_memories: list[dict[str, Any]] = []
    filtered_memories: list[dict[str, Any]] = []
    influence_trace: list[dict[str, Any]] = []

    scored: list[tuple[float, str, dict[str, Any]]] = []
    for memory in memories:
        score, reason = _score_memory(query_terms, memory)
        scored.append((score, reason, memory))

    scored.sort(key=lambda item: item[0], reverse=True)

    for score, reason, memory in scored:
        enriched = {
            **memory,
            "score": score,
            "reason": reason,
        }
        if score > 0:
            selected_memories.append(enriched)
            influence_trace.append(
                {
                    "memory_id": memory.get("id"),
                    "effect": "changed_next_step",
                    "reason": reason,
                    "score": score,
                }
            )
        else:
            filtered_memories.append(
                {
                    "id": memory.get("id"),
                    "reason": reason,
                    "score": score,
                }
            )

    top_memory = selected_memories[0]["id"] if selected_memories else None
    next_step = (
        f"Use top memory {top_memory} and {len(selected_memories)} selected memories to act on: {query}"
        if selected_memories
        else f"Proceed without memory influence for: {query}"
    )

    return {
        "query": query,
        "selected_memories": selected_memories,
        "filtered_memories": filtered_memories,
        "influence_trace": influence_trace,
        "decision": {
            "objective": query,
            "next_step": next_step,
        },
    }
