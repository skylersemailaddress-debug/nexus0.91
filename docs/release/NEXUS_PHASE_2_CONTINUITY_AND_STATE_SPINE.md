# NEXUS PHASE 2 — CONTINUITY AND STATE SPINE

Status: OPEN
Authority: Release execution phase for Enterprise-Launchable AI OS progression.

## Purpose

This phase closes the first launch-critical runtime truth category after the release constitution and enterprise gate are in place.

Continuity is not satisfied by stored chat history alone.
Continuity is satisfied only when Nexus can restart and reconstruct the real state of the active mission, including:
- current objective
- current trajectory
- current next step
- pending blockers
- pending approvals
- current run/job state
- relevant artifacts
- operator-visible summary surfaces

If continuity is partial, generic, guessed, or restart-fragile, this phase fails.

## Phase Target

Move the `continuity` category in `docs/release/NEXUS_SCORECARD.json` from structural-only to evidence-backed operational truth.

## Non-Negotiable Deliverables

### 1. Durable message append
Must exist:
- message append path persists user and system turns durably
- append path preserves ordering and actor identity
- append path can be replayed into continuity state reconstruction

Fails if:
- messages are transient
- ordering is unstable
- append can succeed without durable persistence

### 2. Resume snapshot generation
Must exist:
- one canonical resume snapshot builder
- snapshot includes objective, next step, current trajectory, pending blockers, approvals, active runs/jobs, and relevant artifacts
- snapshot is generated from persisted state, not guessed from chat wording

Fails if:
- snapshot is shallow
- snapshot omits active runtime state
- snapshot is assembled from heuristics without state grounding

### 3. Objective resolution
Must exist:
- one canonical objective resolver
- objective is restorable after restart
- objective is inspectable by operator surfaces

Fails if:
- objective is null when mission state exists
- objective differs after restart without justified state change

### 4. Next-step resolution
Must exist:
- one canonical next-step resolver
- next step is deterministic and derived from current persisted state
- next step changes only when underlying state changes

Fails if:
- next step is generic
- next step is guessed from recency alone
- next step changes between resumes without real state transition

### 5. Continuity scenario tests
Must exist:
- restart-active-mission scenario
- restart-with-pending-approval scenario
- restart-with-active-run scenario
- resume-summary-completeness scenario

Fails if:
- scenario coverage is missing
- continuity is only structurally tested
- evidence is not emitted

## Required Validators

The following validators must exist or be upgraded in this phase:
- `scripts/validate_continuity.py`
- `scripts/run_continuity_scenarios.py`
- `scripts/validate_nexus_enterprise.py` integration for continuity evidence

## Required Evidence Artifacts

Evidence must be emitted under:
- `docs/release/evidence/continuity/restart_active_mission.json`
- `docs/release/evidence/continuity/restart_with_pending_approval.json`
- `docs/release/evidence/continuity/restart_with_active_run.json`
- `docs/release/evidence/continuity/resume_summary_completeness.json`

## Required Tests

At minimum:
- `tests/test_continuity_resume_snapshot.py`
- `tests/test_continuity_objective_resolution.py`
- `tests/test_continuity_next_step_resolution.py`
- `tests/test_continuity_restart_scenarios.py`

## Implementation Guidance

This phase should bind the continuity spine across the existing architecture layers:
- shell conversation/session layer
- mission state model
- runtime run/job state
- persistence layer
- operator summary surfaces

The continuity spine must become a canonical path, not duplicated heuristics spread across UI, shell, and runtime.

## Pass Condition

This phase passes only when all are true simultaneously:
- durable message append is real
- resume snapshot is state-derived and complete
- objective restoration is correct
- next-step restoration is deterministic
- continuity scenarios pass after restart
- evidence artifacts exist
- enterprise validator accepts continuity proof inputs

## Automatic Fail Conditions

Any of the following keeps this phase open:
- resume depends on shallow summary text
- objective or next step is null despite active mission state
- restart loses approvals, blockers, runs, or artifacts
- operator surfaces show continuity claims not backed by persisted state
- continuity evidence is missing or stale

## Score Impact

This phase is the primary route to increasing:
- `enterprise_launchable_ai_os.continuity`
- `enterprise_launchable_ai_os.system_truth`
- `enterprise_launchable_ai_os.behavioral_proof`
- `enterprise_launchable_ai_os.no_overclaim`

## Next Phase Dependency

Memory behavior integration may not be marked complete until this continuity phase is operational, because memory influence must attach to a stable persisted mission/resume context.
