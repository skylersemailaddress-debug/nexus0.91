from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_OUT = ROOT / "docs" / "release" / "evidence" / "release_hardening" / "release_summary.json"
CERT_REPORT_OUT = ROOT / "docs" / "release" / "evidence" / "release" / "release_hardening_report.json"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {"ok": False, "missing": str(path)}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {"ok": False, "invalid": str(path)}


def main() -> int:
    SUMMARY_OUT.parent.mkdir(parents=True, exist_ok=True)
    CERT_REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)

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
    certification_report = {
        "passed": ok,
        "checks": [
            {"name": name, "passed": bool(value), "details": [] if value else ["failed"]}
            for name, value in checks.items()
        ],
        "summary_path": str(SUMMARY_OUT.relative_to(ROOT)),
    }

    SUMMARY_OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    CERT_REPORT_OUT.write_text(json.dumps(certification_report, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
