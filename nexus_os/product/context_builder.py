from __future__ import annotations

from typing import Any


def build_context(*, query: str, memories: list[dict[str, Any]]) -> dict[str, Any]:
    query_terms = {term for term in query.lower().split() if term}

    selected_memories: list[dict[str, Any]] = []
    filtered_memories: list[dict[str, Any]] = []
    influence_trace: list[dict[str, Any]] = []

    scored: list[tuple[float, dict[str, Any]]] = []
    for memory in memories:
        content = str(memory.get("content", ""))
        content_terms = set(content.lower().split())
        overlap = len(query_terms.intersection(content_terms))
        score = float(overlap)
        scored.append((score, memory))

    scored.sort(key=lambda item: item[0], reverse=True)

    for score, memory in scored:
        enriched = {
            **memory,
            "score": score,
            "reason": "term_overlap" if score > 0 else "low_relevance",
        }
        if score > 0:
            selected_memories.append(enriched)
            influence_trace.append(
                {
                    "memory_id": memory.get("id"),
                    "effect": "changed_next_step",
                    "reason": "selected_for_context",
                }
            )
        else:
            filtered_memories.append(
                {
                    "id": memory.get("id"),
                    "reason": "low_relevance",
                }
            )

    next_step = (
        f"Use {len(selected_memories)} selected memories to act on: {query}"
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
