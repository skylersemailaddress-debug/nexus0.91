from __future__ import annotations

import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nexus_os.product.context_builder import build_context

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "memory"
REPORT_PATH = EVIDENCE_DIR / "memory_trace_report.json"
CONTRADICTED = "contradicted"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _memory(
    memory_id: str,
    content: str,
    trust: int = 2,
    recency: int = 2,
    truth_state: str = "active",
    supersedes: str | None = None,
) -> dict[str, Any]:
    for module_name in ("nexus_os.product.memory_model", "nexus_os.memory.memory_model", "nexus_os.memory"):
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        build_memory = getattr(module, "build_memory", None)
        if build_memory is not None:
            try:
                return build_memory(
                    memory_id=memory_id,
                    content=content,
                    trust=trust,
                    recency=recency,
                    truth_state=truth_state,
                    supersedes=supersedes,
                ).to_dict()
            except TypeError:
                return build_memory(memory_id=memory_id, content=content, trust=trust, recency=recency).to_dict()
    payload: dict[str, Any] = {
        "id": memory_id,
        "content": content,
        "source": "runtime",
        "trust": trust,
        "recency": recency,
        "truth_state": truth_state,
    }
    if supersedes:
        payload["supersedes"] = supersedes
    return payload


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    memories = [
        _memory("mem-active", "optimize deployment pipeline for speed", trust=2, recency=2),
        _memory("mem-duplicate", "optimize deployment pipeline for speed", trust=1, recency=1, supersedes="mem-active"),
        _memory("mem-contradicted", "do not optimize deployment pipeline for speed", trust=1, recency=1, truth_state=CONTRADICTED),
        _memory("mem-irrelevant", "refresh brand homepage", trust=1, recency=1),
    ]
    query = "optimize deployment pipeline"
    context = build_context(query=query, memories=memories)
    selected_ids = [m.get("id") for m in context.get("selected_memories", [])]
    suppressed_ids = [m.get("id") for m in context.get("suppressed_memories", [])]
    filtered_ids = [m.get("id") for m in context.get("filtered_memories", [])]
    trace_ids = [item.get("memory_id") for item in context.get("influence_trace", [])]
    checks = [
        {"name": "active_memory_selected", "passed": selected_ids == ["mem-active"]},
        {"name": "duplicate_not_selected", "passed": "mem-duplicate" not in selected_ids and "mem-duplicate" in suppressed_ids},
        {"name": "contradicted_not_selected", "passed": "mem-contradicted" not in selected_ids and "mem-contradicted" in filtered_ids},
        {"name": "contradicted_not_traced", "passed": "mem-contradicted" not in trace_ids},
        {"name": "trace_matches_selection", "passed": trace_ids == selected_ids},
    ]
    report = {
        "generated_at": _timestamp(),
        "query": query,
        "selected_ids": selected_ids,
        "suppressed_ids": suppressed_ids,
        "filtered_ids": filtered_ids,
        "trace_ids": trace_ids,
        "context": context,
        "checks": checks,
        "passed": all(check["passed"] for check in checks),
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
