from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from nexus_os.product.job_store import persist_job, load_job
from nexus_os.product.run_lifecycle import pause_run, resume_run, restore_runs

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "execution"
REPORT_PATH = EVIDENCE_DIR / "interrupt_resume_report.json"


def _ts():
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    job = {
        "id": "job-ir-1",
        "runs": [{"id": "run-1", "status": "running", "events": [], "attempt_count": 1}],
    }

    paused = pause_run(job, "run-1")
    persist_job(paused)

    restored = load_job("job-ir-1")
    restored2 = restore_runs(restored)
    resumed = resume_run(restored2, "run-1")

    run = resumed["runs"][0]
    passed = (
        run.get("status") == "running"
        and any(e.get("type") == "paused" for e in run.get("events", []))
        and any(e.get("type") == "restored" for e in run.get("events", []))
        and any(e.get("type") == "resumed" for e in run.get("events", []))
    )

    report = {"generated_at": _ts(), "job": job, "result": resumed, "passed": passed}
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
