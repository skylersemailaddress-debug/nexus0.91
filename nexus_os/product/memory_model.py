from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ACTIVE = "active"
SUPERSEDED = "superseded"
CONTRADICTED = "contradicted"
STALE = "stale"


@dataclass
class DurableMemory:
    id: str
    content: str
    source: str = "runtime"
    trust: int = 1
    recency: int = 1
    semantic_key: str = ""
    truth_state: str = ACTIVE
    supersedes: str | None = None
    contradictory_to: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "source": self.source,
            "trust": self.trust,
            "recency": self.recency,
            "semantic_key": self.semantic_key,
            "truth_state": self.truth_state,
            "supersedes": self.supersedes,
            "contradictory_to": self.contradictory_to,
        }


def normalize_memory_text(text: str) -> str:
    normalized = " ".join(text.lower().split())
    for token in ".,;:!?()[]{}\"'":
        normalized = normalized.replace(token, "")
    return normalized.strip()


def semantic_key_for_text(text: str) -> str:
    normalized = normalize_memory_text(text)
    tokens = sorted(token for token in normalized.split() if token)
    return " ".join(tokens)


def build_memory(
    *,
    memory_id: str,
    content: str,
    source: str = "runtime",
    trust: int = 1,
    recency: int = 1,
    truth_state: str = ACTIVE,
    supersedes: str | None = None,
    contradictory_to: str | None = None,
) -> DurableMemory:
    return DurableMemory(
        id=memory_id,
        content=content,
        source=source,
        trust=trust,
        recency=recency,
        semantic_key=semantic_key_for_text(content),
        truth_state=truth_state,
        supersedes=supersedes,
        contradictory_to=contradictory_to,
    )


def deduplicate_memories(memories: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    active_by_key: dict[str, dict[str, Any]] = {}
    suppressed: list[dict[str, Any]] = []

    for memory in memories:
        key = str(memory.get("semantic_key") or semantic_key_for_text(str(memory.get("content", ""))))
        enriched = {
            **memory,
            "semantic_key": key,
        }
        existing = active_by_key.get(key)
        if existing is None:
            active_by_key[key] = enriched
            continue

        existing_score = int(existing.get("trust", 1) or 1) + int(existing.get("recency", 1) or 1)
        candidate_score = int(enriched.get("trust", 1) or 1) + int(enriched.get("recency", 1) or 1)
        if candidate_score > existing_score:
            suppressed.append({**existing, "suppression_reason": "deduplicated"})
            active_by_key[key] = {**enriched, "supersedes": existing.get("id")}
        else:
            suppressed.append({**enriched, "suppression_reason": "deduplicated", "supersedes": existing.get("id")})

    return {
        "active": list(active_by_key.values()),
        "suppressed": suppressed,
    }


def resolve_contradictions(memories: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    active: list[dict[str, Any]] = []
    suppressed: list[dict[str, Any]] = []

    grouped: dict[str, list[dict[str, Any]]] = {}
    for memory in memories:
        source_key = str(memory.get("semantic_key") or semantic_key_for_text(str(memory.get("content", ""))))
        grouped.setdefault(source_key, []).append(memory)

    for _, group in grouped.items():
        contradictory = [m for m in group if m.get("truth_state") == CONTRADICTED]
        non_contradictory = [m for m in group if m.get("truth_state") != CONTRADICTED]

        if contradictory and non_contradictory:
            winner = max(non_contradictory, key=lambda m: int(m.get("trust", 1) or 1) + int(m.get("recency", 1) or 1))
            active.append(winner)
            for item in group:
                if item is not winner:
                    suppressed.append({**item, "suppression_reason": "contradicted_or_inactive"})
        else:
            winner = max(group, key=lambda m: int(m.get("trust", 1) or 1) + int(m.get("recency", 1) or 1))
            active.append(winner)
            for item in group:
                if item is not winner:
                    suppressed.append({**item, "suppression_reason": "lower_priority"})

    return {
        "active": active,
        "suppressed": suppressed,
    }
