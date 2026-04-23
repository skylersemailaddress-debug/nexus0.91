from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from nexus_os.product.artifact_lineage import bind_artifact, build_lineage_report

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "execution"
REPORT_PATH = EVIDENCE_DIR / "artifact_lineage_report.json"


def _timestamp():
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    job = {
        "id": "job-1",
        "runs": [{"id": "run-1"}],
        "artifacts": [],
    }

    artifact = {"id": "artifact-1", "type": "log"}

    updated = bind_artifact(job, "run-1", artifact)
    report_data = build_lineage_report(updated)

    passed = (
        report_data.get("artifact_count") == 1
        and report_data.get("lineage", [])[0].get("run_id") == "run-1"
    )

    report = {
        "generated_at": _timestamp(),
        "report": report_data,
        "passed": passed,
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
