from __future__ import annotations

import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import _repo_bootstrap  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover
    from scripts import _repo_bootstrap  # noqa: F401
from nexus_os.product.context_builder import build_context

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "memory"
REPORT_PATH = EVIDENCE_DIR / "memory_behavior_report.json"


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
    base = build_context(query=query, memories=[])
    variant = build_context(
        query=query,
        memories=[_memory("mem1", "optimize deployment pipeline aggressively", trust=2, recency=2)],
    )
    base_next = (base.get("decision") or {}).get("next_step")
    variant_next = (variant.get("decision") or {}).get("next_step")
    changed = bool(base_next and variant_next and base_next != variant_next)
    checks = [
        {"name": "base_has_no_selected_memories", "passed": base.get("selected_memories") == []},
        {"name": "variant_selects_memory", "passed": bool(variant.get("selected_memories"))},
        {"name": "variant_has_influence_trace", "passed": bool(variant.get("influence_trace"))},
        {"name": "decision_changed_by_memory", "passed": changed},
    ]
    report = {
        "generated_at": _timestamp(),
        "base": base,
        "variant": variant,
        "behavior_changed": changed,
        "checks": checks,
        "passed": all(check["passed"] for check in checks),
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
