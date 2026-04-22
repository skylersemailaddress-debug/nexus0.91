# Phase 10 Factory Work Package

## Objective
Add factory generation for specs, scaffolds, docs, tests, assets, and release manifests with validation before trust.

## Required outcomes
- spec generation
- scaffold generation
- docs generation
- tests generation
- assets generation
- release manifest generation
- validation before trust
- update loop support

## Implementation tasks
1. Add factory engine.
2. Add factory generation route.
3. Add factory scenario and validator.
4. Wire factory into behavioral runtime.

## Validation tasks
- generation must return spec, scaffold, docs, tests, assets, manifest
- manifest must be present
- validator must pass

## Blockers
Phase 10 is not complete if generated output is decorative or unvalidated.
