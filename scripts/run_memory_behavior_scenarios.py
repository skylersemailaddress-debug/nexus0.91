from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from nexus_os.product.context_builder import build_context
from nexus_os.product.memory_model import build_memory

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "memory"
REPORT_PATH = EVIDENCE_DIR / "memory_behavior_report.json"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_case(memories):
    return build_context(query="optimize deployment pipeline", memories=memories)


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    base = run_case([])

    mem_variant = [
        build_memory(memory_id="mem1", content="optimize deployment pipeline aggressively", trust=2, recency=2).to_dict()
    ]

    variant = run_case(mem_variant)

    changed = base.get("decision") != variant.get("decision")

    report = {
        "generated_at": _timestamp(),
        "base": base,
        "variant": variant,
        "behavior_changed": changed,
        "passed": changed,
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if changed else 1


if __name__ == "__main__":
    raise SystemExit(main())
