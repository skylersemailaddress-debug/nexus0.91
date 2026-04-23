from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "jobs"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def _job_path(job_id: str) -> Path:
    return DATA_DIR / f"{job_id}.json"


def persist_job(job: dict[str, Any]) -> None:
    job_id = str(job.get("id"))
    path = _job_path(job_id)
    path.write_text(json.dumps(job, indent=2), encoding="utf-8")


def load_job(job_id: str) -> dict[str, Any] | None:
    path = _job_path(job_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def list_jobs() -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    for file in DATA_DIR.glob("*.json"):
        jobs.append(json.loads(file.read_text(encoding="utf-8")))
    return jobs
