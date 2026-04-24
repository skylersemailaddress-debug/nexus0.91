from __future__ import annotations

from typing import Any


def _terms(value: str) -> set[str]:
    return {
        term.strip(".,:;!?()[]{}\"'").lower()
        for term in str(value).split()
        if term.strip(".,:;!?()[]{}\"'")
    }


def _memory_id(memory: dict[str, Any]) -> str | None:
    value = memory.get("id") or memory.get("memory_id")
    return str(value) if value is not None else None


def _content_key(memory: dict[str, Any]) -> str:
    content = str(memory.get("content") or memory.get("text") or "")
    return " ".join(sorted(_terms(content)))


def build_context(*, query: str, memories: list[dict[str, Any]]) -> dict[str, Any]:
    query_terms = _terms(query)

    selected_memories: list[dict[str, Any]] = []
    filtered_memories: list[dict[str, Any]] = []
    suppressed_memories: list[dict[str, Any]] = []
    influence_trace: list[dict[str, Any]] = []
    seen_content: dict[str, str | None] = {}

    scored: list[tuple[float, dict[str, Any]]] = []
    for memory in memories:
        memory_id = _memory_id(memory)
        truth_state = str(memory.get("truth_state") or "active").lower()
        if truth_state in {"contradicted", "stale", "inactive", "retracted"}:
            filtered_memories.append({"id": memory_id, "reason": f"suppressed_as_{truth_state}"})
            continue

        content_key = _content_key(memory)
        supersedes = memory.get("supersedes")
        if supersedes:
            suppressed_memories.append({**memory, "suppression_reason": "deduplicated"})
            continue
        if content_key and content_key in seen_content:
            suppressed_memories.append({**memory, "supersedes": seen_content[content_key], "suppression_reason": "deduplicated"})
            continue

        content = str(memory.get("content") or memory.get("text") or "")
        content_terms = _terms(content)
        overlap_terms = sorted(query_terms.intersection(content_terms))
        score = float(len(overlap_terms))
        if content_key:
            seen_content[content_key] = memory_id
        scored.append((score, {**memory, "matched_terms": overlap_terms}))

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
                    "memory_id": _memory_id(memory),
                    "effect": "changed_next_step",
                    "reason": "selected_for_context",
                    "matched_terms": memory.get("matched_terms", []),
                    "score": score,
                    "truth_state": memory.get("truth_state", "active"),
                }
            )
        else:
            filtered_memories.append({"id": _memory_id(memory), "reason": "low_relevance", "score": score})

    next_step = (
        f"Use {len(selected_memories)} selected memories to act on: {query}"
        if selected_memories
        else f"Proceed without memory influence for: {query}"
    )

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
