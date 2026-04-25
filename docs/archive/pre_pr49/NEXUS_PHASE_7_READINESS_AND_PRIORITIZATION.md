> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# NEXUS PHASE 7 — READINESS AND PRIORITIZATION

Status: OPEN
Authority: Release execution phase for Enterprise-Launchable AI OS progression.

## Purpose

This phase closes the readiness category required for Nexus to behave like an active intelligence that knows what matters now rather than a passive state container.

Readiness is not satisfied by displaying many items, recent items, or static task lists.
Readiness is satisfied only when Nexus can rank what matters now, what changed, what needs action, and what is likely next, in ways that are materially correct, explainable, state-backed, and useful.

If important items are buried, ordering is random, or readiness is presentation-only, this phase fails.

## Phase Target

Move the `readiness` category in `docs/release/NEXUS_SCORECARD.json` from structural-only to evidence-backed behavioral truth.

## Non-Negotiable Deliverables

### 1. Canonical readiness ranking path
Must exist:
- one canonical readiness ranking path used by primary surfaced priorities
- ranking consumes continuity, execution, approvals, memory influence, and state-change signals
- ranking outputs are stable enough to be explainable and auditable

Fails if:
- different surfaces rank important items differently without justification
- readiness is hand-authored or hard-coded outside canonical logic
- ranking cannot be reconstructed after the fact

### 2. What-matters-now correctness
Must exist:
- system can surface the highest-priority active objective, blocker, risk, approval, or execution need
- surfaced items materially reflect current state and consequences of inaction
- readiness is sensitive to time, blockage, execution state, and user impact

Fails if:
- trivial items outrank blocked critical work
- surfaced top item is not actionable or materially important
- high-priority issues are buried below cosmetic or stale items

### 3. What-changed and what-needs-action truth
Must exist:
- system can surface important state changes since last interaction or checkpoint
- system can identify action-requiring changes separately from informational changes
- surfaced changes map to real underlying state transitions

Fails if:
- changes are omitted or misclassified
- informational noise overwhelms actionable changes
- readiness cannot distinguish change from action need

### 4. Likely-next prediction quality
Must exist:
- system can identify likely next operational need or decision point based on current trajectory
- likely-next output is grounded in continuity, execution, approvals, and memory-informed context
- prediction is explainable and bounded

Fails if:
- likely-next is generic, shallow, or random
- likely-next is disconnected from actual state trajectory
- prediction is presented confidently without basis

### 5. Readiness explanation and inspection
Must exist:
- readiness surfaces can explain why an item is ranked highly
- explanation can reference the contributing state, memory, approval, execution, or change signals
- operators can inspect ranking reasons where appropriate

Fails if:
- ordering is opaque
- operator cannot reconstruct why a priority surfaced
- explanations are generic and not state-linked

### 6. Readiness scenario tests
Must exist:
- blocked-critical-work outranks low-importance activity scenario
- approval-required-item surfaces above passive updates scenario
- state-change-actionability classification scenario
- likely-next reflects execution trajectory scenario
- readiness explanation matches ranking inputs scenario

Fails if:
- scenario coverage is missing
- readiness is only structurally tested
- evidence is not emitted

## Required Validators

The following validators must exist or be upgraded in this phase:
- `scripts/validate_readiness.py`
- `scripts/run_readiness_scenarios.py`
- `scripts/validate_nexus_enterprise.py` integration for readiness evidence

## Required Evidence Artifacts

Evidence must be emitted under:
- `docs/release/evidence/readiness/blocked_critical_work_priority.json`
- `docs/release/evidence/readiness/approval_required_priority.json`
- `docs/release/evidence/readiness/change_actionability_classification.json`
- `docs/release/evidence/readiness/likely_next_from_execution_trajectory.json`
- `docs/release/evidence/readiness/readiness_explanation_integrity.json`

## Required Tests

At minimum:
- `tests/test_readiness_priority_ranking.py`
- `tests/test_readiness_change_detection.py`
- `tests/test_readiness_actionability_classification.py`
- `tests/test_readiness_likely_next.py`
- `tests/test_readiness_explanations.py`

## Implementation Guidance

This phase should bind the readiness spine across the existing architecture layers:
- continuity snapshot outputs
- execution runtime state
- approvals and governance state
- ranked memory context and influence traces
- operator and workspace surfaced priorities
- UI truth bindings

Readiness must become a canonical ranking and explanation path, not a presentation layer heuristic.

## Pass Condition

This phase passes only when all are true simultaneously:
- canonical readiness ranking path is real
- what matters now, what changed, what needs action, and what is likely next are surfaced correctly
- readiness explanations are real and inspectable
- readiness scenarios pass
- evidence artifacts exist
- enterprise validator accepts readiness proof inputs

## Automatic Fail Conditions

Any of the following keeps this phase open:
- important work is buried beneath low-impact items
- approval or blocker urgency is not reflected in surfaced priorities
- likely-next is generic or disconnected from state trajectory
- explanations do not match the real ranking inputs
- readiness evidence is missing or stale

## Score Impact

This phase is the primary route to increasing:
- `enterprise_launchable_ai_os.readiness`
- `enterprise_launchable_ai_os.behavioral_proof`
- `enterprise_launchable_ai_os.ui_truth`
- `enterprise_launchable_ai_os.observability`
- `enterprise_launchable_ai_os.no_overclaim`

## Next Phase Dependency

Release hardening should not be marked complete until readiness is operational, because enterprise launch claims require the surfaced operating picture to be materially correct under real runtime conditions rather than structurally present only.
