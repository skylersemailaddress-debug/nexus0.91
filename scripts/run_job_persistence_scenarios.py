from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from nexus_os.product.job_store import persist_job, load_job, list_jobs

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "execution"
REPORT_PATH = EVIDENCE_DIR / "job_persistence_report.json"


def _timestamp():
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    job = {
        "id": "job-1",
        "runs": [
            {"id": "run-1", "status": "running"}
        ],
    }

    persist_job(job)

    restored = load_job("job-1")
    jobs = list_jobs()

    passed = (
        restored is not None
        and restored.get("runs", [])[0].get("id") == "run-1"
        and any(j.get("id") == "job-1" for j in jobs)
    )

    report = {
        "generated_at": _timestamp(),
        "job": job,
        "restored": restored,
        "jobs": jobs,
        "passed": passed,
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
