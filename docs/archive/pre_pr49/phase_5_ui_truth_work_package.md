> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# Phase 5 UI Truth Work Package

## Objective
Ensure all core operator surfaces are backed by live runtime state and evidence rather than decorative placeholders.

## Required outcomes
- approvals backed by real runtime state
- mission backed by real runtime state
- memory backed by real runtime state
- progress backed by runs and attempts
- proof backed by artifacts and evidence
- no decorative core surfaces

## Implementation tasks
1. Add a consolidated operator surface endpoint.
2. Return mission, approvals, memory context, run progress, and proof from live state.
3. Bind proof IDs to real run artifacts and capability evidence.
4. Upgrade UI truth scenario to assert runtime-backed operator surface fields.
5. Add a Phase 5 UI truth validator.

## Validation tasks
- ui truth scenario must pass
- operator surface must expose non-placeholder mission
- approvals must be explicitly runtime-backed
- progress must include run counts or active runs
- proof must include real proof IDs or evidence references
- memory influence must be surfaced from live memory context

## Blockers
Phase 5 is not complete if operator surfaces can render without evidence-backed runtime state.
