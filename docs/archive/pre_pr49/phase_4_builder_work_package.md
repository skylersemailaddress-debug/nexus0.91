> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# Phase 4 Builder Work Package

## Objective
Upgrade Nexus from a stateful execution substrate into a capability builder that generates useful outputs, validates them before use, and exposes a reusable capability registry.

## Required outcomes
- generate useful capabilities from goals
- validate generated capabilities before trust
- expose a capability registry with status and evidence
- maintain/update generated capabilities over time
- builder scenario proves generation, validation, registry presence, and update loop behavior

## Implementation tasks
1. Add builder routes for capability generation, validation, listing, and updating.
2. Persist generated capability records with title, goal, output, validation status, and evidence.
3. Expose a registry endpoint returning all capabilities.
4. Bind validation evidence to each capability.
5. Upgrade behavioral builder scenario to assert usefulness, validation, and registry integration.

## Validation tasks
- builder scenario must pass
- generated capability must include non-empty output
- validation step must mark capability as validated
- registry must contain generated capability
- update step must revise capability and append maintenance evidence

## Blockers
Phase 4 is not complete if capabilities can be generated without validation, or if the registry is decorative rather than backed by live capability records.
