> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# Phase 1 Continuity Work Package

## Objective
Finish the continuity and state spine before any later phase work.

## Required outcomes
- durable `/messages/append`
- trustworthy `/projects/default/resume`
- resolved objective
- resolved next step
- scenario-level continuity proof

## Implementation tasks
1. Fix message append storage path so meta payloads persist safely.
2. Ensure append survives restart/re-entry.
3. Ensure resume returns recent messages, objective, and next step.
4. Remove null/fallback-only resume behavior.
5. Bind continuity scenario to fail on shallow resume.

## Validation tasks
- continuity scenario must pass
- resume must expose non-null objective
- resume must expose non-null next step
- appended probe message must be visible in continuity evidence

## Blockers
No later phase may be called 10/10 until this package passes.
