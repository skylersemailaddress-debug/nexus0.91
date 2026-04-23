from __future__ import annotations

from copy import deepcopy
from typing import Any


def bind_artifact(job: dict[str, Any], run_id: str, artifact: dict[str, Any]) -> dict[str, Any]:
    updated = deepcopy(job)
    updated.setdefault("artifacts", [])
    lineage_item = {
        **artifact,
        "run_id": run_id,
        "job_id": updated.get("id"),
    }
    updated["artifacts"].append(lineage_item)

    for run in updated.get("runs", []):
        if run.get("id") == run_id:
            run.setdefault("artifact_ids", []).append(artifact.get("id"))
            run.setdefault("events", []).append({"type": "artifact_bound", "artifact_id": artifact.get("id")})
            return updated

    raise KeyError(run_id)


def build_lineage_report(job: dict[str, Any]) -> dict[str, Any]:
    artifacts = list(job.get("artifacts", []))
    runs = list(job.get("runs", []))
    lineage = []
    for artifact in artifacts:
        lineage.append(
            {
                "artifact_id": artifact.get("id"),
                "run_id": artifact.get("run_id"),
                "job_id": artifact.get("job_id"),
            }
        )
    return {
        "job_id": job.get("id"),
        "run_count": len(runs),
        "artifact_count": len(artifacts),
        "lineage": lineage,
    }
