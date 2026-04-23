# NEXUS PHASE 5 — EXECUTION TRUTH

Status: OPEN
Authority: Release execution phase for Enterprise-Launchable AI OS progression.

## Purpose

This phase closes the execution truth category required for Nexus to behave like a real operating system rather than a conversational planner.

Execution is not satisfied by describing work, producing plans, or simulating task flow.
Execution is satisfied only when Nexus can create real runs/jobs, persist them, pause/resume them, retry/repair them, bind artifacts and evidence to them, and surface truthful runtime state through restart and interruption.

If execution mostly exists as chat or inferred progress, this phase fails.

## Phase Target

Move the `execution` category in `docs/release/NEXUS_SCORECARD.json` from structural-only to evidence-backed operational truth.

## Non-Negotiable Deliverables

### 1. Canonical run and job state model
Must exist:
- one canonical run model
- one canonical job model
- lifecycle states are explicit and persisted
- operator/runtime/UI surfaces consume the same underlying run/job truth

Fails if:
- multiple subsystems maintain conflicting execution state
- job state is implicit or recomputed from chat/summaries only
- lifecycle transitions are not reconstructable

### 2. Persistent execution across interruption
Must exist:
- active runs/jobs survive restart and interruption
- checkpoint or recovery state exists where required
- resumed execution continues from persisted state rather than starting over

Fails if:
- interruption causes silent restart from scratch
- progress is lost between sessions
- resumed execution is guessed rather than recovered

### 3. Pause, resume, retry, repair, revalidate loop
Must exist:
- execution can be paused intentionally
- execution can resume from a paused state
- failed work can enter retry or repair paths
- repaired work is revalidated before completion

Fails if:
- failure paths terminate without structured recovery
- retry is ad hoc or not persisted
- completion can occur without validation after repair

### 4. Artifact and evidence lineage
Must exist:
- runs/jobs bind produced artifacts to execution lineage
- evidence is attached to execution outcomes
- operator surfaces can inspect artifact provenance where appropriate

Fails if:
- artifacts exist without execution provenance
- execution claims completion without evidence
- artifacts cannot be traced to the originating run/job

### 5. Approval and policy hooks inside execution
Must exist:
- risky execution can pause on approval or policy gate
- execution state reflects blocked or waiting status truthfully
- policy/approval transitions are persisted and auditable

Fails if:
- execution bypasses approvals or policy requirements
- blocked state exists only in UI and not runtime
- approvals cannot resume the intended execution path

### 6. Execution scenario tests
Must exist:
- interrupt-and-resume-run scenario
- pause-and-resume-job scenario
- fail-repair-revalidate scenario
- artifact-lineage-integrity scenario
- approval-blocked-execution scenario

Fails if:
- scenario coverage is missing
- execution is only structurally tested
- evidence is not emitted

## Required Validators

The following validators must exist or be upgraded in this phase:
- `scripts/validate_execution_resume.py`
- `scripts/run_execution_scenarios.py`
- `scripts/validate_nexus_enterprise.py` integration for execution evidence

## Required Evidence Artifacts

Evidence must be emitted under:
- `docs/release/evidence/execution/resume_run.json`
- `docs/release/evidence/execution/pause_resume_job.json`
- `docs/release/evidence/execution/fail_repair_revalidate.json`
- `docs/release/evidence/execution/artifact_lineage_integrity.json`
- `docs/release/evidence/execution/approval_blocked_execution.json`

## Required Tests

At minimum:
- `tests/test_execution_run_state_machine.py`
- `tests/test_execution_pause_resume.py`
- `tests/test_execution_retry_repair_revalidate.py`
- `tests/test_execution_artifact_lineage.py`
- `tests/test_execution_approval_policy_hooks.py`

## Implementation Guidance

This phase should bind the execution spine across the existing architecture layers:
- runtime run/job state machine
- persistence layer
- approvals and governance hooks
- artifact model
- operator summary surfaces
- continuity resume snapshot
- memory-informed planning inputs

Execution truth must become a canonical path, not duplicated heuristics spread across shell, runtime, operator projection, and UI.

## Pass Condition

This phase passes only when all are true simultaneously:
- canonical run/job state is real
- execution survives interruption and restart
- pause/resume/retry/repair/revalidate loop is operational
- artifact and evidence lineage exist
- approval/policy hooks are real inside execution
- execution scenarios pass
- evidence artifacts exist
- enterprise validator accepts execution proof inputs

## Automatic Fail Conditions

Any of the following keeps this phase open:
- execution progress is implied but not persisted
- interruption loses run/job state
- repair paths are informal or non-revalidating
- artifacts are detached from runtime lineage
- UI implies execution state not backed by persisted runtime truth
- execution evidence is missing or stale

## Score Impact

This phase is the primary route to increasing:
- `enterprise_launchable_ai_os.execution`
- `enterprise_launchable_ai_os.behavioral_proof`
- `enterprise_launchable_ai_os.system_truth`
- `enterprise_launchable_ai_os.approvals_control`
- `enterprise_launchable_ai_os.observability`
- `enterprise_launchable_ai_os.no_overclaim`

## Next Phase Dependency

UI truth should not be marked complete until execution truth is operational, because mission progress, approvals, blockers, artifacts, and active work surfaces must bind to real runtime execution state rather than projected shell expectations.
