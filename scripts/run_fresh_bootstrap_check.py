from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "release" / "evidence" / "release_hardening" / "fresh_bootstrap_report.json"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    checks = [
        {"name": "pyproject_present", "passed": (ROOT / "pyproject.toml").exists()},
        {"name": "package_present", "passed": (ROOT / "nexus_os").is_dir()},
        {"name": "enterprise_gate_present", "passed": (ROOT / "scripts" / "run_enterprise_gate.py").exists()},
    ]
    report = {
        "ok": all(check["passed"] for check in checks),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
