> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# NEXUS PHASE 8 — RELEASE HARDENING

Status: OPEN
Authority: Release execution phase for Enterprise-Launchable AI OS progression.

## Purpose

This phase closes the release hardening category required for Nexus to be credibly launchable rather than technically interesting but operationally fragile.

Release hardening is not satisfied by passing local tests, manual setup success, or optimistic launch claims.
Release hardening is satisfied only when Nexus can be installed cleanly, booted without manual fixes, validated through CI and enterprise gate checks, rolled back safely, and packaged with evidence showing what is proven and what is not.

If launch depends on environment hacks, manual rescue steps, or undocumented operator intervention, this phase fails.

## Phase Target

Move the `release_hardening` category in `docs/release/NEXUS_SCORECARD.json` from structural-only to evidence-backed operational truth.

## Non-Negotiable Deliverables

### 1. Clean install path
Must exist:
- one documented clean install path for supported environments
- install path succeeds without manual fixes or hidden steps
- install path includes required dependencies, environment setup, and validation entrypoints

Fails if:
- install depends on undocumented local state
- setup requires ad hoc patching or trial-and-error
- fresh environment cannot reproduce expected system state

### 2. Clean boot path
Must exist:
- supported launch paths boot without manual intervention
- startup failures are visible and fail closed
- required runtime dependencies are checked explicitly

Fails if:
- launch requires manual rescue steps
- silent partial boot is possible
- startup assumptions are not validated

### 3. CI and validator gating
Must exist:
- CI covers core release-critical checks
- enterprise validator is part of release gating
- failing proof or missing evidence blocks launch claims

Fails if:
- CI passes while release-critical truth is broken
- enterprise gate is optional or bypassed
- launch labeling does not depend on validator output

### 4. Rollback readiness
Must exist:
- rollback path is documented and testable
- rollback can recover from bad release states
- rollback evidence exists for supported release paths

Fails if:
- deployment can only move forward
- rollback is theoretical only
- failed release leaves state or operator surfaces inconsistent

### 5. Evidence bundle completeness
Must exist:
- release evidence bundle captures constitution status, scorecard state, proof scenario outputs, and known open failures
- missing or failing proof is represented honestly
- release package can be audited after the fact

Fails if:
- release bundle omits failing areas
- evidence exists only informally or manually
- claimed maturity exceeds bundled proof

### 6. Release hardening scenario tests
Must exist:
- clean-install-from-fresh-environment scenario
- clean-boot-with-required-dependency-checks scenario
- enterprise-gate-blocks-invalid-release scenario
- rollback-recovers-prior-good-state scenario
- evidence-bundle-integrity scenario

Fails if:
- scenario coverage is missing
- hardening is only structurally tested
- evidence is not emitted

## Required Validators

The following validators must exist or be upgraded in this phase:
- `scripts/validate_release.py`
- `scripts/run_release_scenarios.py`
- `scripts/validate_nexus_enterprise.py` integration for release hardening evidence

## Required Evidence Artifacts

Evidence must be emitted under:
- `docs/release/evidence/release/clean_install.json`
- `docs/release/evidence/release/clean_boot.json`
- `docs/release/evidence/release/enterprise_gate_blocks_invalid_release.json`
- `docs/release/evidence/release/rollback_recovery.json`
- `docs/release/evidence/release/evidence_bundle_integrity.json`

## Required Tests

At minimum:
- `tests/test_release_clean_install.py`
- `tests/test_release_clean_boot.py`
- `tests/test_release_gate_enforcement.py`
- `tests/test_release_rollback.py`
- `tests/test_release_evidence_bundle.py`

## Implementation Guidance

This phase should bind the release hardening spine across the existing architecture layers:
- install/bootstrap scripts
- supported launchers and runtime entrypoints
- CI workflows and release validators
- enterprise gate outputs
- evidence bundle generation
- rollback and recovery procedures

Release hardening must become a canonical launch path with verifiable evidence, not an operator-memory process.

## Pass Condition

This phase passes only when all are true simultaneously:
- clean install path is real
- clean boot path is real
- CI and enterprise validator gate launch claims
- rollback is testable and works
- release evidence bundle is complete and honest
- release hardening scenarios pass
- evidence artifacts exist
- enterprise validator accepts release hardening proof inputs

## Automatic Fail Conditions

Any of the following keeps this phase open:
- launch requires hidden manual intervention
- CI does not reflect real release-critical truth
- enterprise gate can be bypassed without consequence
- rollback is undocumented or untested
- evidence bundle is incomplete, stale, or misleading

## Score Impact

This phase is the primary route to increasing:
- `enterprise_launchable_ai_os.release_hardening`
- `enterprise_launchable_ai_os.behavioral_proof`
- `enterprise_launchable_ai_os.no_overclaim`
- `enterprise_launchable_ai_os.enterprise_standard`
- `enterprise_launchable_ai_os.system_truth`

## Next Phase Dependency

Security and governance hardening should not be marked complete until release hardening is operational, because credible launch readiness requires the system to fail closed, ship honest evidence, and recover safely under bad release conditions.
