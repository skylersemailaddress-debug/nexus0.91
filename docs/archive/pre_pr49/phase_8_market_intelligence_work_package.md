> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# Phase 8 Market Intelligence Work Package

## Objective
Add real market intelligence flow with signal ingestion, normalization, scoring, and ranked opportunities.

## Required outcomes
- signal ingestion path
- normalized market item structure
- scoring model
- ranked opportunities output
- traceable ranking reasons
- scenario proving ranked output

## Implementation tasks
1. Add market intelligence engine.
2. Add ingest and opportunity endpoints.
3. Store normalized signals in runtime.
4. Add scenario and validator.
5. Wire into behavioral runtime.

## Validation tasks
- ingest must accept signals
- opportunities endpoint must return ranked items
- each item must include score and reasons
- scenario must pass
- validator must pass

## Blockers
Phase 8 is not complete if opportunities are decorative or unranked.
