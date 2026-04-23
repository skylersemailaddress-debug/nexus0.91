from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


VALID_JOB_STATES = {
    "pending",
    "running",
    "paused",
    "waiting",
    "failed",
    "repairing",
    "revalidated",
    "complete",
    "blocked",
    "resumed",
}

VALID_RUN_STATES = {
    "pending",
    "active",
    "paused",
    "blocked",
    "failed",
    "repairing",
    "recovered",
    "complete",
    "resumed",
}


@dataclass
class JobRecord:
    id: str
    status: str
    current_step: str
    retries: int = 0
    blocked_by_approval: bool = False
    repair_notes: List[str] = field(default_factory=list)

    def normalize(self) -> None:
        if self.status not in VALID_JOB_STATES:
            self.status = "pending"


@dataclass
class RunRecord:
    id: str
    objective: str
    status: str
    jobs: List[JobRecord] = field(default_factory=list)
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    approvals: List[Dict[str, Any]] = field(default_factory=list)

    def normalize(self) -> None:
        if self.status not in VALID_RUN_STATES:
            self.status = "pending"
        for job in self.jobs:
            job.normalize()


def create_run(state: Dict[str, Any], run_id: str, objective: str, current_step: str) -> RunRecord:
    job = JobRecord(id=f"{run_id}-job-1", status="running", current_step=current_step)
    run = RunRecord(id=run_id, objective=objective, status="active", jobs=[job])
    run.normalize()
    state.setdefault("runs", []).append(asdict(run))
    return run


def load_run(run_data: Dict[str, Any]) -> RunRecord:
    jobs = [JobRecord(**job) for job in run_data.get("jobs", [])]
    run = RunRecord(
        id=str(run_data.get("id", "run-unknown")),
        objective=str(run_data.get("objective", "No objective")),
        status=str(run_data.get("status", "pending")),
        jobs=jobs,
        artifacts=list(run_data.get("artifacts", [])),
        approvals=list(run_data.get("approvals", [])),
    )
    run.normalize()
    return run


def persist_run(state: Dict[str, Any], run: RunRecord) -> None:
    runs = state.setdefault("runs", [])
    payload = asdict(run)
    for index, existing in enumerate(runs):
        if existing.get("id") == run.id:
            runs[index] = payload
            return
    runs.append(payload)


def pause_job(run: RunRecord, job_id: str) -> None:
    for job in run.jobs:
        if job.id == job_id:
            job.status = "paused"
            return


def resume_job(run: RunRecord, job_id: str) -> None:
    for job in run.jobs:
        if job.id == job_id:
            job.status = "resumed"
            return


def block_run_for_approval(run: RunRecord, approval_id: str, summary: str) -> None:
    run.status = "blocked"
    run.approvals.append({"id": approval_id, "status": "pending", "summary": summary})
    for job in run.jobs:
        job.status = "waiting"
        job.blocked_by_approval = True


def resume_after_approval(run: RunRecord, approval_id: str) -> None:
    for approval in run.approvals:
        if approval.get("id") == approval_id:
            approval["status"] = "approved"
    run.status = "active"
    for job in run.jobs:
        if job.blocked_by_approval:
            job.blocked_by_approval = False
            job.status = "resumed"


def fail_job(run: RunRecord, job_id: str, note: str) -> None:
    run.status = "failed"
    for job in run.jobs:
        if job.id == job_id:
            job.status = "failed"
            job.repair_notes.append(note)
            return


def repair_and_revalidate_job(run: RunRecord, job_id: str, repair_note: str) -> None:
    run.status = "recovered"
    for job in run.jobs:
        if job.id == job_id:
            job.status = "revalidated"
            job.retries += 1
            job.repair_notes.append(repair_note)
            return


def add_artifact(run: RunRecord, artifact_id: str, parent: Optional[str], kind: str = "evidence") -> None:
    run.artifacts.append({"id": artifact_id, "parent": parent, "type": kind})


def resume_run(run: RunRecord) -> None:
    run.status = "resumed"
    for job in run.jobs:
        if job.status in {"paused", "waiting", "running"}:
            job.status = "running" if job.status == "running" else "resumed"


def build_execution_snapshot(run: RunRecord, reasoning: List[str]) -> Dict[str, Any]:
    return {
        "run": asdict(run),
        "jobs": [asdict(job) for job in run.jobs],
        "artifacts": list(run.artifacts),
        "reasoning": reasoning,
        "passed": True,
    }
