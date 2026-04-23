from __future__ import annotations

from typing import Any

from .memory_model import deduplicate_memories, resolve_contradictions


def _normalize_terms(text: str) -> set[str]:
    cleaned: set[str] = set()
    for term in text.split():
        normalized = term.strip(".,:;!?()[]{}\"").strip("'").lower()
        if normalized:
            cleaned.add(normalized)
    return cleaned


def build_context(*, query: str, memories: list[dict[str, Any]]) -> dict[str, Any]:
    query_terms = _normalize_terms(query)

    dedup = deduplicate_memories(memories)
    dedup_active = dedup["active"]

    resolved = resolve_contradictions(dedup_active)
    active_memories = resolved["active"]
    suppressed_memories = dedup["suppressed"] + resolved["suppressed"]

    selected_memories: list[dict[str, Any]] = []
    filtered_memories: list[dict[str, Any]] = []
    influence_trace: list[dict[str, Any]] = []

    scored: list[tuple[float, dict[str, Any], str]] = []
    for memory in active_memories:
        content = str(memory.get("content", memory.get("text", "")))
        content_terms = _normalize_terms(content)
        overlap_terms = sorted(query_terms.intersection(content_terms))
        overlap = len(overlap_terms)
        trust = float(memory.get("trust", 1) or 1)
        recency = float(memory.get("recency", 1) or 1)
        score = float(overlap) + (0.25 * trust) + (0.25 * recency)
        reason = "term_overlap" if overlap > 0 else "low_relevance"
        enriched = {
            **memory,
            "content": content,
            "score": score,
            "matched_terms": overlap_terms,
            "reason": reason,
        }
        scored.append((score, enriched, reason))

    scored.sort(key=lambda item: item[0], reverse=True)

    for score, memory, reason in scored:
        if reason == "term_overlap":
            selected_memories.append(memory)
            influence_trace.append(
                {
                    "memory_id": memory.get("id"),
                    "effect": "changed_next_step",
                    "reason": "selected_for_context",
                    "matched_terms": memory.get("matched_terms", []),
                    "score": score,
                    "truth_state": memory.get("truth_state", "active"),
                }
            )
        else:
            filtered_memories.append(
                {
                    "id": memory.get("id"),
                    "reason": "low_relevance",
                    "score": score,
                }
            )

    if selected_memories:
        memory_summary = "; ".join(
            f"{memory.get('id', 'memory')}:{','.join(memory.get('matched_terms', []))}"
            for memory in selected_memories
        )
        next_step = f"Use memory-backed context for: {query} [{memory_summary}]"
    else:
        next_step = f"Proceed without memory influence for: {query}"

    return {
        "query": query,
        "selected_memories": selected_memories,
        "filtered_memories": filtered_memories,
        "suppressed_memories": suppressed_memories,
        "influence_trace": influence_trace,
        "decision": {
            "objective": query,
            "next_step": next_step,
            "memory_influenced": bool(selected_memories),
            "selected_memory_count": len(selected_memories),
            "suppressed_memory_count": len(suppressed_memories),
        },
    }
