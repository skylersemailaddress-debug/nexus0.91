from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EVIDENCE = {
    ROOT / "docs" / "release" / "evidence" / "ui" / "ui_master_truth_report.json": {
        "ok": False,
        "source": "bootstrap_provisional",
        "checks": {"ui_truth_locked": False},
        "errors": ["bootstrap evidence must be replaced by real generated proof"],
    },
    ROOT / "docs" / "release" / "evidence" / "behavioral_gate" / "behavioral_ten_ten_report.json": {
        "ok": False,
        "source": "bootstrap_provisional",
        "checks": {"behavioral_gate_present": False},
        "errors": ["bootstrap evidence must be replaced by real generated proof"],
    },
}


def main() -> None:
    for path, payload in EVIDENCE.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
