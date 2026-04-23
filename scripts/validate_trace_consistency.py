from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_LOG = ROOT / "docs" / "release" / "evidence" / "runtime" / "audit_log.jsonl"
OUT = ROOT / "docs" / "release" / "evidence" / "runtime" / "trace_consistency_report.json"


def main() -> int:
    result = {"ok": True, "checks": {}, "errors": []}
    records = []
    if AUDIT_LOG.exists():
        for line in AUDIT_LOG.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                records.append(json.loads(line))

    request_ok = True
    trace_ok = True
    missing = 0
    for record in records:
        trace = record.get("trace", {})
        if not isinstance(trace, dict):
            missing += 1
            request_ok = False
            trace_ok = False
            continue
        if not trace.get("request_id"):
            request_ok = False
            missing += 1
        if not trace.get("trace_id"):
            trace_ok = False
            missing += 1

    result["checks"] = {
        "audit_log_exists": AUDIT_LOG.exists(),
        "request_ids_present": request_ok,
        "trace_ids_present": trace_ok,
        "records_checked": len(records),
        "missing_trace_fields": missing,
    }

    if not AUDIT_LOG.exists():
        result["ok"] = False
        result["errors"].append("audit log missing")
    if not request_ok:
        result["ok"] = False
        result["errors"].append("missing request_id in audit log")
    if not trace_ok:
        result["ok"] = False
        result["errors"].append("missing trace_id in audit log")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
