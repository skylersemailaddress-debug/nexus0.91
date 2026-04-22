from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    indicator_files = [
        ROOT / "docs" / "release" / "phase_6_release_hardening_work_package.md",
        ROOT / "scripts" / "run_release_hardening.py",
    ]

    missing = [str(p) for p in indicator_files if not p.exists()]
    ok = not missing

    result = {"ok": ok, "missing": missing}

    out = ROOT / "docs" / "release" / "evidence" / "release_hardening" / "rollback_readiness_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))

    print(json.dumps(result, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
