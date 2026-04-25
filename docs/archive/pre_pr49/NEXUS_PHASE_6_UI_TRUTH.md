> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# NEXUS PHASE 6 — UI TRUTH

Status: OPEN
Authority: Release execution phase for Enterprise-Launchable AI OS progression.

## Purpose

This phase closes the UI truth category required for Nexus to behave like a truthful operating environment rather than a decorative shell.

UI truth is not satisfied by strong design language, doctrine alignment, or polished interaction alone.
UI truth is satisfied only when every visible mission, progress, approval, memory, readiness, and artifact surface is backed by real runtime state and disappears, collapses, or changes correctly as that state changes.

If the UI implies work, memory, approvals, readiness, or execution that are not backed by real state, this phase fails.

## Phase Target

Move the `ui_truth` category in `docs/release/NEXUS_SCORECARD.json` from structural-only to evidence-backed operational truth.

## Non-Negotiable Deliverables

### 1. Canonical UI-to-runtime binding
Must exist:
- each operational UI surface binds to one canonical runtime or state source
- UI does not maintain conflicting shadow truth for mission, runs, approvals, memory, or artifacts
- state changes propagate to visible surfaces correctly

Fails if:
- UI caches or invents state that diverges from runtime truth
- the same concept is derived differently across surfaces
- important UI state cannot be traced to a canonical backing source

### 2. Mission and progress truth
Must exist:
- mission view reflects actual objective, trajectory, blockers, and next step
- progress surfaces reflect real run/job state rather than inferred completion
- progress changes as execution changes

Fails if:
- mission/progress surfaces are static or guessed
- UI shows progress without persisted execution backing
- objective or next step shown in UI differs from canonical continuity state

### 3. Approval and intervention truth
Must exist:
- approvals surface reflects real blocked/waiting/approved runtime state
- intervention points are tied to real execution or policy gates
- approval actions change runtime state correctly

Fails if:
- approvals are cosmetic or informational only
- blocked state exists in UI but not in runtime
- UI can imply an approval path that does not affect execution

### 4. Memory and readiness truth
Must exist:
- memory surfaces reflect real ranked memory context or influence traces
- readiness surfaces reflect real ranking and prioritization state
- hidden, suppressed, or irrelevant memory is not presented as active intelligence context

Fails if:
- memory UI is decorative or disconnected from causal influence
- readiness ordering is static, random, or presentation-only
- UI overstates memory intelligence or prioritization correctness

### 5. Artifact and proof truth
Must exist:
- artifact surfaces reflect real outputs with execution lineage where appropriate
- proof/release surfaces reflect emitted evidence rather than doctrine claims
- missing proof is shown honestly

Fails if:
- artifacts appear complete without lineage
- release/proof surfaces imply passing state without evidence
- UI hides missing evidence behind presentation polish

### 6. Relevance-driven and adaptive surface behavior
Must exist:
- non-relevant surfaces collapse, recede, or disappear
- workspace remains primary; operator/depth surfaces are summoned appropriately
- UI adapts to current state without becoming cluttered or fake-dashboard oriented

Fails if:
- irrelevant static panels persist
- chat/composer is the only truth surface despite live operational state existing
- adaptive behavior is hard-coded rather than state-driven where it matters

### 7. UI truth scenario tests
Must exist:
- mission-surface-matches-runtime scenario
- approval-surface-matches-runtime scenario
- progress-surface-matches-run-state scenario
- memory-surface-matches-influence-trace scenario
- proof-surface-matches-evidence scenario

Fails if:
- scenario coverage is missing
- UI is only structurally tested
- evidence is not emitted

## Required Validators

The following validators must exist or be upgraded in this phase:
- `scripts/validate_ui_truth.py`
- `scripts/run_ui_truth_scenarios.py`
- `scripts/validate_nexus_enterprise.py` integration for UI truth evidence

## Required Evidence Artifacts

Evidence must be emitted under:
- `docs/release/evidence/ui/mission_surface_matches_runtime.json`
- `docs/release/evidence/ui/approval_surface_matches_runtime.json`
- `docs/release/evidence/ui/progress_surface_matches_run_state.json`
- `docs/release/evidence/ui/memory_surface_matches_influence_trace.json`
- `docs/release/evidence/ui/proof_surface_matches_evidence.json`

## Required Tests

At minimum:
- `tests/test_ui_mission_runtime_binding.py`
- `tests/test_ui_approval_runtime_binding.py`
- `tests/test_ui_progress_runtime_binding.py`
- `tests/test_ui_memory_truth_binding.py`
- `tests/test_ui_proof_truth_binding.py`

## Implementation Guidance

This phase should bind the UI truth spine across the existing architecture layers:
- shell workspace/composer surfaces
- operator projection surfaces
- continuity snapshot outputs
- execution runtime state
- approval and governance state
- ranked memory and readiness outputs
- release evidence surfaces

UI truth must become a canonical projection of underlying runtime truth, not a parallel narrative layer.

## Pass Condition

This phase passes only when all are true simultaneously:
- canonical UI-to-runtime binding is real
- mission, progress, approval, memory, readiness, and artifact/proof surfaces are truthful
- non-relevant surfaces recede correctly
- UI truth scenarios pass
- evidence artifacts exist
- enterprise validator accepts UI truth proof inputs

## Automatic Fail Conditions

Any of the following keeps this phase open:
- UI claims progress not backed by run/job state
- UI claims memory intelligence not backed by influence traces
- UI claims approval state not backed by runtime or governance state
- release/proof UI exceeds evidence state
- static or decorative operational panels remain in core surfaces
- UI truth evidence is missing or stale

## Score Impact

This phase is the primary route to increasing:
- `enterprise_launchable_ai_os.ui_truth`
- `enterprise_launchable_ai_os.behavioral_proof`
- `enterprise_launchable_ai_os.no_overclaim`
- `enterprise_launchable_ai_os.readiness`
- `enterprise_launchable_ai_os.observability`

## Next Phase Dependency

Readiness should not be marked complete until UI truth is operational, because the surfaced ranking of what matters now, what changed, and what needs action must be displayed through truthful state-bound UI rather than detached logic or static presentation.
