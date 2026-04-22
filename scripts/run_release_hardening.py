from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "release" / "evidence" / "release_hardening" / "release_summary.json"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {"ok": False, "missing": str(path)}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {"ok": False, "invalid": str(path)}


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    bootstrap = load_json(ROOT / "docs" / "release" / "evidence" / "release_hardening" / "fresh_bootstrap_report.json")
    rollback = load_json(ROOT / "docs" / "release" / "evidence" / "release_hardening" / "rollback_readiness_report.json")
    behavioral = load_json(ROOT / "docs" / "release" / "evidence" / "behavioral_runtime" / "behavioral_scenarios_report.json")

    checks = {
        "bootstrap": bootstrap.get("ok", False),
        "rollback": rollback.get("ok", False),
        "behavioral_runtime": behavioral.get("ok", False),
    }

    ok = all(checks.values())

    summary = {
        "ok": ok,
        "checks": checks,
        "sources": {
            "bootstrap": bootstrap,
            "rollback": rollback,
            "behavioral": behavioral,
        },
    }

    OUT.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
