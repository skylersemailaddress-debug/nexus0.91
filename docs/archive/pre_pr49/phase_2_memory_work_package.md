> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# Phase 2 Memory Work Package

## Objective
Upgrade memory from storage/retrieval into behavior-changing context integration.

## Required outcomes
- memory retrieval is used in context build
- selected memory is ranked
- memory influence is traceable
- junk or low-value memory is filtered or downranked
- downstream decision/state reflects selected memory

## Implementation tasks
1. Add context-build contract route.
2. Return selected memories, scores, and influence trace.
3. Return filtered memories with reasons.
4. Bind decision/next-step output to selected memories.
5. Upgrade behavioral memory scenario to assert influence, not just retrieval.

## Validation tasks
- memory influence validator must pass
- memory scenario must pass
- context response must include selected_memories, filtered_memories, influence_trace, decision
- inserted relevant memory must appear in selected_memories
- junk memory must not dominate selected_memories

## Blockers
Phase 2 is not complete if memory only stores and retrieves without changing context or decision behavior.
