# NEXUS PHASE 14 — FINAL CONFIGURATION CORRECTNESS

Status: OPEN
Authority: Release execution phase for 10/10 Final Nexus progression.

## Purpose

This phase closes the final configuration correctness category required for Nexus to operate in its best and intended configuration rather than merely functioning with inconsistent defaults, weak thresholds, or partially aligned policies.

Final configuration correctness is not satisfied by passing subsystem tests alone.
Final configuration correctness is satisfied only when the integrated system runs with the correct defaults, thresholds, routing, policies, prioritization behavior, operator surfaces, and fail-closed settings so that the product behaves as intended under real conditions without hidden tuning debt.

If the system works only with manual tuning, fragile local assumptions, or inconsistent configuration choices, this phase fails.

## Phase Target

Move the `final_nexus_ten_ten.final_configuration_correctness` category in `docs/release/NEXUS_SCORECARD.json` from structural-only to evidence-backed operational truth.

## Non-Negotiable Deliverables

### 1. Canonical configuration ownership
Must exist:
- major runtime, policy, prioritization, UI, and release-affecting configuration has canonical ownership
- configuration sources are explicit and non-conflicting
- defaults reflect intended product behavior rather than development convenience

Fails if:
- multiple configuration paths conflict silently
- important behavior depends on hidden or local-only settings
- defaults are not aligned with intended product truth

### 2. Correct default behavior under clean launch
Must exist:
- clean install and clean boot produce the intended product behavior without manual tuning
- routing, prioritization, approvals, UI behavior, and safety boundaries are sensible by default
- default configuration supports truthful enterprise-launchable operation

Fails if:
- first boot behavior is wrong or materially degraded without manual edits
- product defaults optimize for convenience over truth or safety
- important product behavior depends on undocumented environment shaping

### 3. Threshold, policy, and ranking calibration correctness
Must exist:
- readiness thresholds, policy gates, memory ranking behaviors, and adaptation bounds are calibrated to intended product behavior
- configuration choices are explainable and consistent with doctrine and release truth
- calibration is evidence-backed rather than arbitrary

Fails if:
- thresholds produce obviously wrong priorities or behavior
- policy gates are too permissive or too brittle by default
- memory, readiness, or learning behavior is miscalibrated despite otherwise working subsystems

### 4. Operator and recovery configuration correctness
Must exist:
- operator intervention paths, recovery paths, and release controls behave correctly under default configuration
- configuration supports diagnosis, rollback, and corrective action without hidden switches
- operator-facing behavior matches runtime and governance truth

Fails if:
- recovery depends on special local flags or undocumented knobs
- operator controls behave differently across environments without explicit reason
- default configuration weakens diagnosis or recovery capability

### 5. Final configuration scenario tests
Must exist:
- clean-launch-default-behavior-correctness scenario
- readiness-and-policy-threshold-calibration scenario
- memory-and-adaptation-bound-calibration scenario
- operator-recovery-default-path scenario
- cross-environment-configuration-consistency scenario

Fails if:
- scenario coverage is missing
- configuration correctness is only structurally tested
- evidence is not emitted

## Required Validators

The following validators must exist or be upgraded in this phase:
- `scripts/validate_final_configuration_correctness.py`
- `scripts/run_final_configuration_scenarios.py`
- `scripts/validate_nexus_enterprise.py` integration for final configuration evidence

## Required Evidence Artifacts

Evidence must be emitted under:
- `docs/release/evidence/final_configuration/clean_launch_default_behavior_correctness.json`
- `docs/release/evidence/final_configuration/readiness_and_policy_threshold_calibration.json`
- `docs/release/evidence/final_configuration/memory_and_adaptation_bound_calibration.json`
- `docs/release/evidence/final_configuration/operator_recovery_default_path.json`
- `docs/release/evidence/final_configuration/cross_environment_configuration_consistency.json`

## Required Tests

At minimum:
- `tests/test_final_configuration_ownership.py`
- `tests/test_final_configuration_defaults.py`
- `tests/test_final_configuration_thresholds_and_policy.py`
- `tests/test_final_configuration_operator_recovery.py`
- `tests/test_final_configuration_cross_environment_consistency.py`

## Implementation Guidance

This phase should bind the final configuration correctness spine across the existing architecture layers:
- runtime and policy configuration
- readiness, memory, and adaptation calibration
- UI and operator defaults
- recovery and release controls
- cross-environment launch and validation behavior
- enterprise gate and release labeling outputs

Final configuration correctness must become a product-truth calibration layer, not a late manual tuning exercise.

## Pass Condition

This phase passes only when all are true simultaneously:
- canonical configuration ownership is real
- clean launch defaults are correct
- thresholds, policy, and ranking calibration are correct
- operator and recovery configuration is correct
- final configuration scenarios pass
- evidence artifacts exist
- enterprise validator accepts final configuration proof inputs

## Automatic Fail Conditions

Any of the following keeps this phase open:
- important behavior depends on hidden or conflicting configuration paths
- clean launch produces materially wrong default behavior
- thresholds or policy defaults are miscalibrated
- operator or recovery paths require undocumented configuration changes
- final configuration evidence is missing or stale

## Score Impact

This phase is the primary route to increasing:
- `final_nexus_ten_ten.final_configuration_correctness`
- `enterprise_launchable_ai_os.no_overclaim`
- `enterprise_launchable_ai_os.system_truth`
- `enterprise_launchable_ai_os.enterprise_standard`

## Next Phase Dependency

Final validation and 10/10 certification should not be marked complete until final configuration correctness is operational, because certification is not credible while default behavior, thresholds, or control paths remain misconfigured or environment-dependent.
