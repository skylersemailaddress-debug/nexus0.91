# Phase 7 Intelligence Work Package

## Objective
Turn Nexus into a traceable intelligence layer that synthesizes continuity, memory, execution, and builder state into usable plans.

## Required outcomes
- context synthesis from continuity + memory + execution + builder state
- decision output that is more than pass-through text
- next-step generation backed by system state
- intelligence trace showing why the system chose a path
- scenario proving usable plans from live state

## Implementation tasks
1. Add an intelligence engine module.
2. Add a planning endpoint returning objective, context summary, recommended action, next step, and trace.
3. Add an intelligence scenario that seeds live state before planning.
4. Add an intelligence validator.
5. Wire intelligence into the behavioral runtime report.

## Validation tasks
- intelligence scenario must pass
- plan response must contain non-empty context summary
- recommended action must be non-empty
- next step must be non-empty
- trace must expose messages_used, memories_used, runs_considered, capabilities_considered

## Blockers
Phase 7 is not complete if planning is opaque or merely echoes the input objective without using live system state.
