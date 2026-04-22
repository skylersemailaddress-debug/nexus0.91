from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    required = [
        ROOT / "scripts" / "run_behavioral_scenarios.py",
        ROOT / "scripts" / "validate_behavioral_runtime.py",
        ROOT / "nexus_os" / "product" / "api_server.py",
    ]

    missing = [str(path) for path in required if not path.exists()]
    ok = not missing
    result = {"ok": ok, "missing": missing}
    out = ROOT / "docs" / "release" / "evidence" / "release_hardening" / "fresh_bootstrap_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
