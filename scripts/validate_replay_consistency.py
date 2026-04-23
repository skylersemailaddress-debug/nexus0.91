from __future__ import annotations

import json
from pathlib import Path

from nexus_os.observability.replay import replay_audit_log
from nexus_os.persistence.store import load_state

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "release" / "evidence" / "runtime" / "replay_consistency_report.json"


def main() -> int:
    replay = replay_audit_log()
    state = load_state()
    result = {
        "ok": True,
        "checks": {
            "message_count_match": replay.get("messages") == len(state.get("messages", [])),
            "memory_count_match": replay.get("memories") == len(state.get("memories", [])),
            "run_count_match": replay.get("runs") == len(state.get("runs", {})),
        },
        "errors": [],
    }
    for name, ok in result["checks"].items():
        if not ok:
            result["ok"] = False
            result["errors"].append(f"{name} failed")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
