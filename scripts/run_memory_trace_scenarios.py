from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from nexus_os.product.context_builder import build_context
from nexus_os.product.memory_model import build_memory, CONTRADICTED

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "memory"
REPORT_PATH = EVIDENCE_DIR / "memory_trace_report.json"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    memories = [
        build_memory(memory_id="mem-active", content="optimize deployment pipeline for speed", trust=2, recency=2).to_dict(),
        build_memory(memory_id="mem-duplicate", content="optimize deployment pipeline for speed", trust=1, recency=1).to_dict(),
        build_memory(memory_id="mem-contradicted", content="do not optimize deployment pipeline for speed", trust=1, recency=1, truth_state=CONTRADICTED).to_dict(),
        build_memory(memory_id="mem-irrelevant", content="refresh brand homepage", trust=1, recency=1).to_dict(),
    ]

    query = "optimize deployment pipeline"
    context = build_context(query=query, memories=memories)

    selected = context.get("selected_memories", [])
    suppressed = context.get("suppressed_memories", [])
    filtered = context.get("filtered_memories", [])
    trace = context.get("influence_trace", [])

    selected_ids = [m.get("id") for m in selected]
    suppressed_ids = [m.get("id") for m in suppressed]
    filtered_ids = [m.get("id") for m in filtered]
    trace_ids = [item.get("memory_id") for item in trace]

    passed = (
        "mem-active" in selected_ids
        and "mem-duplicate" in suppressed_ids
        and "mem-contradicted" in filtered_ids  # contradicted memories go to filtered_memories after GATE1
        and trace_ids == ["mem-active"]
    )

    report = {
        "generated_at": _timestamp(),
        "query": query,
        "selected_ids": selected_ids,
        "suppressed_ids": suppressed_ids,
        "filtered_ids": filtered_ids,
        "trace_ids": trace_ids,
        "context": context,
        "passed": passed,
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
