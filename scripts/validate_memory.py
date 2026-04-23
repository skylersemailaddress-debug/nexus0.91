from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "memory"

REQUIRED_FILES = [
    "memory_context_integration_report.json",
    "memory_trace_report.json",
    "memory_behavior_report.json",
]


def main() -> int:
    missing = []
    failures = []

    for name in REQUIRED_FILES:
        path = EVIDENCE_DIR / name
        if not path.exists():
            missing.append(name)
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if not data.get("passed"):
            failures.append(name)

    if missing:
        print(f"Missing memory evidence: {missing}")
        return 1

    if failures:
        print(f"Failing memory evidence: {failures}")
        return 1

    print("Memory gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
