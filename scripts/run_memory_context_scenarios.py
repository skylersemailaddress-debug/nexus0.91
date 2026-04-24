from __future__ import annotations

import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nexus_os.product.context_builder import build_context

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "memory"
REPORT_PATH = EVIDENCE_DIR / "memory_context_integration_report.json"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _memory(memory_id: str, content: str, trust: int = 2, recency: int = 2) -> dict[str, Any]:
    for module_name in ("nexus_os.product.memory_model", "nexus_os.memory.memory_model", "nexus_os.memory"):
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        build_memory = getattr(module, "build_memory", None)
        if build_memory is not None:
            return build_memory(memory_id=memory_id, content=content, trust=trust, recency=recency).to_dict()
    return {
        "id": memory_id,
        "content": content,
        "source": "runtime",
        "trust": trust,
        "recency": recency,
        "truth_state": "active",
    }


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    query = "optimize deployment pipeline"
    without_memory = build_context(query=query, memories=[])
    with_memory = build_context(
        query=query,
        memories=[_memory("mem-1", "optimize deployment pipeline for speed")],
    )
    selected = with_memory.get("selected_memories", [])
    trace = with_memory.get("influence_trace", [])
    decision_without = without_memory.get("decision", {})
    decision_with = with_memory.get("decision", {})
    checks = [
        {"name": "without_memory_has_no_selected_memories", "passed": without_memory.get("selected_memories") == []},
        {"name": "with_memory_selects_relevant_memory", "passed": bool(selected) and selected[0].get("id") == "mem-1"},
        {"name": "with_memory_has_influence_trace", "passed": bool(trace) and trace[0].get("memory_id") == "mem-1"},
        {"name": "decision_changes_with_memory", "passed": decision_without.get("next_step") != decision_with.get("next_step")},
    ]
    report = {
        "generated_at": _timestamp(),
        "query": query,
        "without_memory": without_memory,
        "with_memory": with_memory,
        "behavior_changed": decision_without.get("next_step") != decision_with.get("next_step"),
        "checks": checks,
        "passed": all(check["passed"] for check in checks),
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
