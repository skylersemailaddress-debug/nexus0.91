from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from nexus_os.product.context_builder import build_context

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "memory"
REPORT_PATH = EVIDENCE_DIR / "memory_context_integration_report.json"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def scenario_without_memory(query: str) -> Dict[str, Any]:
    return build_context(query=query, memories=[])


def scenario_with_memory(query: str) -> Dict[str, Any]:
    memories = [
        {
            "id": "mem-1",
            "content": "optimize deployment pipeline for speed",
            "trust": 2,
            "recency": 2,
        }
    ]
    return build_context(query=query, memories=memories)


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    query = "optimize deployment pipeline"

    without_memory = scenario_without_memory(query)
    with_memory = scenario_with_memory(query)

    changed = without_memory.get("decision") != with_memory.get("decision")

    report = {
        "generated_at": _timestamp(),
        "query": query,
        "without_memory": without_memory,
        "with_memory": with_memory,
        "behavior_changed": changed,
        "passed": changed,
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if changed else 1


if __name__ == "__main__":
    raise SystemExit(main())
