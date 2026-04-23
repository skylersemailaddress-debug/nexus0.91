from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "execution"
DEFAULT_REPORT_PATH = DEFAULT_EVIDENCE_DIR / "execution_validation_report.json"

REQUIRED = [
    "resume_run.json",
    "pause_resume_job.json",
    "fail_repair_revalidate.json",
    "artifact_lineage_integrity.json",
    "approval_blocked_execution.json",
]


def _reference_time() -> datetime:
    value = os.getenv("NEXUS_VALIDATION_REFERENCE_TIME", "").strip()
    if not value:
        return datetime.now(UTC)
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).astimezone(UTC)


def _max_age_seconds() -> int:
    raw = os.getenv("NEXUS_EXECUTION_MAX_AGE_SECONDS", "86400").strip()
    try:
        parsed = int(raw)
    except ValueError:
        return 86400
    return parsed if parsed >= 0 else 0


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def _validate_common_payload(data: dict[str, Any], expected_scenario: str) -> list[str]:
    details: list[str] = []

    if data.get("scenario") != expected_scenario:
        details.append("scenario_mismatch")
    if data.get("passed") is not True:
        details.append("passed_flag_false")

    run = data.get("run")
    if not isinstance(run, dict):
        details.append("missing_run")
    else:
        if not run.get("id"):
            details.append("missing_run_id")
        if not run.get("status"):
            details.append("missing_run_status")

    jobs = data.get("jobs")
    if not isinstance(jobs, list) or not jobs:
        details.append("missing_jobs")
    else:
        for index, job in enumerate(jobs):
            if not isinstance(job, dict):
                details.append(f"invalid_job_{index}")
                continue
            if not job.get("id"):
                details.append(f"missing_job_id_{index}")
            if not job.get("status"):
                details.append(f"missing_job_status_{index}")

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list):
        details.append("missing_artifacts")

    reasoning = data.get("reasoning")
    if not isinstance(reasoning, list) or not reasoning:
        details.append("missing_reasoning")

    return details


def _validate_scenario_specific(data: dict[str, Any], expected_scenario: str) -> list[str]:
    details: list[str] = []
    run = data.get("run") if isinstance(data.get("run"), dict) else {}
    jobs = data.get("jobs") if isinstance(data.get("jobs"), list) else []
    artifacts = data.get("artifacts") if isinstance(data.get("artifacts"), list) else []

    if expected_scenario == "resume_run":
        run_status = run.get("status")
        if run_status not in {"resumed", "active"}:
            details.append("resume_run_invalid_status")

    if expected_scenario == "pause_resume_job":
        if not any(isinstance(job, dict) and job.get("status") == "resumed" for job in jobs):
            details.append("pause_resume_job_no_resumed_job")

    if expected_scenario == "fail_repair_revalidate":
        if run.get("status") != "recovered":
            details.append("fail_repair_revalidate_invalid_run_status")
        revalidated = [job for job in jobs if isinstance(job, dict) and job.get("status") == "revalidated"]
        if not revalidated:
            details.append("fail_repair_revalidate_missing_revalidated_job")
        else:
            has_retry = False
            for job in revalidated:
                retries = job.get("retries", 0)
                try:
                    retry_count = int(retries)
                except (TypeError, ValueError):
                    retry_count = 0
                if retry_count >= 1:
                    has_retry = True
                    break
            if not has_retry:
                details.append("fail_repair_revalidate_missing_retry_count")

    if expected_scenario == "artifact_lineage_integrity":
        if not artifacts:
            details.append("artifact_lineage_integrity_missing_artifacts")
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                details.append(f"artifact_lineage_integrity_invalid_artifact_{index}")
                continue
            if not artifact.get("id"):
                details.append(f"artifact_lineage_integrity_missing_artifact_id_{index}")
            if "parent" not in artifact:
                details.append(f"artifact_lineage_integrity_missing_parent_{index}")

    if expected_scenario == "approval_blocked_execution":
        if run.get("status") != "blocked":
            details.append("approval_blocked_execution_run_not_blocked")
        approvals = run.get("approvals")
        if not isinstance(approvals, list) or not approvals:
            details.append("approval_blocked_execution_missing_approvals")

    return details


def _validate_file(path: Path, expected_name: str, ref_time: datetime, max_age_seconds: int) -> dict[str, Any]:
    if not path.exists():
        return {"name": expected_name, "passed": False, "details": ["missing"]}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"name": expected_name, "passed": False, "details": ["invalid_json"]}

    details = _validate_common_payload(data, expected_name.replace(".json", ""))

    ts = _parse_timestamp(data.get("timestamp"))
    if ts is None:
        details.append("missing_or_invalid_timestamp")
    else:
        age_seconds = int((ref_time - ts).total_seconds())
        if age_seconds < -60:
            details.append("future_timestamp")
        elif age_seconds > max_age_seconds:
            details.append("stale")

    details.extend(_validate_scenario_specific(data, expected_name.replace(".json", "")))
    details = sorted(set(details))

    return {"name": expected_name, "passed": not details, "details": details}


def main() -> int:
    evidence_dir = Path(os.getenv("NEXUS_EXECUTION_EVIDENCE_DIR", str(DEFAULT_EVIDENCE_DIR)))
    report_path = Path(os.getenv("NEXUS_EXECUTION_REPORT_PATH", str(DEFAULT_REPORT_PATH)))
    evidence_dir.mkdir(parents=True, exist_ok=True)

    ref_time = _reference_time()
    max_age_seconds = _max_age_seconds()

    checks = [
        _validate_file(evidence_dir / name, name, ref_time, max_age_seconds)
        for name in REQUIRED
    ]

    report = {
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
