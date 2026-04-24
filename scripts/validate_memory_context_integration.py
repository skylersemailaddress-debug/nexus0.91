from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "release" / "evidence" / "memory" / "memory_context_integration_report.json"


def main() -> int:
    if not REPORT_PATH.exists():
        print("Missing memory context integration report")
        return 1
    try:
        data: dict[str, Any] = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Invalid memory context integration report JSON")
        return 1

    checks = data.get("checks")
    if not isinstance(checks, list) or not checks:
        print("Missing memory context checks")
        return 1

    failed = [
        check.get("name", "unknown")
        for check in checks
        if not isinstance(check, dict) or check.get("passed") is not True
    ]
    if data.get("passed") is not True or failed:
        print(f"Memory context integration failed: {failed}")
        return 1

    with_memory = data.get("with_memory", {})
    if not isinstance(with_memory, dict):
        print("Missing with_memory context")
        return 1
    if not with_memory.get("selected_memories"):
        print("No selected memory in memory context")
        return 1
    if not with_memory.get("influence_trace"):
        print("No influence trace in memory context")
        return 1

    print("Memory context integration validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
