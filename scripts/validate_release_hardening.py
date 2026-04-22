from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    summary = ROOT / "docs" / "release" / "evidence" / "release_hardening" / "release_summary.json"

    if not summary.exists():
        print("missing release summary")
        return 1

    data = json.loads(summary.read_text())

    ok = data.get("ok") and all(data.get("checks", {}).values())

    print(json.dumps({"ok": ok}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
