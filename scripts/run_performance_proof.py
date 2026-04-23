from __future__ import annotations

import json
import time
from pathlib import Path

from nexus_os.persistence.store import load_state, save_state
from nexus_os.product.context_builder import build_context

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/release/evidence/runtime/performance_report.json"


def main() -> int:
    state = load_state()

    # expand dataset
    for i in range(100):
        state.setdefault("messages", []).append({"id": f"msg:{i}", "text": f"test {i}"})
        state.setdefault("memories", []).append({"id": f"mem:{i}", "content": f"enterprise runtime {i}"})

    t0 = time.time()
    save_state(state)
    t_save = time.time() - t0

    t1 = time.time()
    _ = load_state()
    t_load = time.time() - t1

    t2 = time.time()
    _ = build_context(query="enterprise runtime", memories=state["memories"])
    t_context = time.time() - t2

    report = {
        "ok": True,
        "source": "generated",
        "metrics": {
            "save_time": t_save,
            "load_time": t_load,
            "context_time": t_context,
            "messages": len(state["messages"]),
            "memories": len(state["memories"]),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
