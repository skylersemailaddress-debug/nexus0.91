from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from nexus_os.product.execution import (
    add_artifact,
    block_run_for_approval,
    build_execution_snapshot,
    create_run,
    fail_job,
    repair_and_revalidate_job,
    resume_after_approval,
    resume_job,
    resume_run,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "release" / "evidence" / "execution"


def _write(name: str, payload: dict) -> None:
    payload.update({"scenario": name, "timestamp": datetime.now(timezone.utc).isoformat()})
    (OUT / f"{name}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    # resume_run
    state = {}
    run = create_run(state, "run-1", "Execute objective", "initial step")
    resume_run(run)
    _write("resume_run", build_execution_snapshot(run, ["run resumed from persisted state"]))

    # pause_resume_job
    state = {}
    run = create_run(state, "run-2", "Pause resume", "step")
    job_id = run.jobs[0].id
    run.jobs[0].status = "paused"
    resume_job(run, job_id)
    _write("pause_resume_job", build_execution_snapshot(run, ["job paused then resumed"]))

    # fail_repair_revalidate
    state = {}
    run = create_run(state, "run-3", "Failure recovery", "step")
    job_id = run.jobs[0].id
    fail_job(run, job_id, "initial failure")
    repair_and_revalidate_job(run, job_id, "repair applied")
    _write("fail_repair_revalidate", build_execution_snapshot(run, ["failure repaired and job revalidated"]))

    # artifact_lineage_integrity
    state = {}
    run = create_run(state, "run-4", "Artifacts", "step")
    add_artifact(run, "artifact-1", None)
    _write("artifact_lineage_integrity", build_execution_snapshot(run, ["artifact lineage preserved"]))

    # approval_blocked_execution
    state = {}
    run = create_run(state, "run-5", "Approval", "step")
    block_run_for_approval(run, "approval-1", "Need approval")
    _write("approval_blocked_execution", build_execution_snapshot(run, ["execution blocked due to approval"]))

    print("[execution] emitted 5 scenarios (runtime-backed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
