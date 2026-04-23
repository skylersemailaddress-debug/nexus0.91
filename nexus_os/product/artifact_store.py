from __future__ import annotations

from typing import Any
from uuid import uuid4


def create_artifact(run_id: str, artifact_type: str, content: str, parent_id: str | None = None) -> dict[str, Any]:
    return {
        "id": str(uuid4()),
        "run_id": run_id,
        "type": artifact_type,
        "content": content,
        "parent_id": parent_id,
    }


def attach_artifact(job: dict[str, Any], run_id: str, artifact: dict[str, Any]) -> dict[str, Any]:
    for run in job.get("runs", []):
        if run.get("id") == run_id:
            run.setdefault("artifacts", []).append(artifact)
            return job
    raise KeyError(run_id)


def build_lineage(run: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts = run.get("artifacts", [])
    by_id = {a["id"]: a for a in artifacts}

    lineage = []
    for artifact in artifacts:
        chain = [artifact]
        parent = artifact.get("parent_id")
        while parent and parent in by_id:
            parent_artifact = by_id[parent]
            chain.append(parent_artifact)
            parent = parent_artifact.get("parent_id")
        lineage.append({
            "artifact_id": artifact["id"],
            "chain": list(reversed(chain)),
        })

    return lineage
