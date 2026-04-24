from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_OUT = ROOT / "docs" / "release" / "evidence" / "release_hardening" / "release_summary.json"
CERT_REPORT_OUT = ROOT / "docs" / "release" / "evidence" / "release" / "release_hardening_report.json"

REQUIRED_REPORTS = {
    "continuity": ROOT / "docs" / "release" / "evidence" / "continuity" / "continuity_validation_report.json",
    "memory_context": ROOT / "docs" / "release" / "evidence" / "memory" / "memory_context_integration_report.json",
    "memory_trace": ROOT / "docs" / "release" / "evidence" / "memory" / "memory_trace_report.json",
    "memory_behavior": ROOT / "docs" / "release" / "evidence" / "memory" / "memory_behavior_report.json",
    "execution": ROOT / "docs" / "release" / "evidence" / "execution" / "execution_validation_report.json",
    "ui_truth": ROOT / "docs" / "release" / "evidence" / "ui" / "ui_validation_report.json",
    "readiness": ROOT / "docs" / "release" / "evidence" / "readiness" / "readiness_validation_report.json",
}


def load_json(path: Path) -> dict:
    if not path.exists():
        return {"passed": False, "missing": str(path)}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"passed": False, "invalid": str(path), "error": str(exc)}


def report_passed(data: dict) -> bool:
    if data.get("passed") is True or data.get("ok") is True:
        checks = data.get("checks")
        if isinstance(checks, list):
            return bool(checks) and all(isinstance(c, dict) and (c.get("passed") is True or c.get("ok") is True) for c in checks)
        if isinstance(checks, dict):
            return bool(checks) and all(value is True for value in checks.values())
        return True
    return False


def main() -> int:
    SUMMARY_OUT.parent.mkdir(parents=True, exist_ok=True)
    CERT_REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)

    sources = {name: load_json(path) for name, path in REQUIRED_REPORTS.items()}
    checks = {name: report_passed(data) for name, data in sources.items()}
    ok = all(checks.values())

    summary = {
        "ok": ok,
        "checks": checks,
        "sources": sources,
    }
    certification_report = {
        "passed": ok,
        "checks": [
            {"name": name, "passed": bool(value), "details": [] if value else ["failed_or_missing"]}
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
