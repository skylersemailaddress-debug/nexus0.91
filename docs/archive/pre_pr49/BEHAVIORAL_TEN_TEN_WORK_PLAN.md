> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# BEHAVIORAL 10/10 WORK PLAN

## Purpose
This file defines the execution path required to move Nexus0.91 from structure-complete to behaviorally proven.

---

## Layer 1 — Gate Enforcement (Immediate)

Replace presence-based validation with behavioral validation.

Required proofs:
- continuity proof
- memory influence proof
- execution persistence proof
- UI truth validation

---

## Layer 2 — Core System Truth

### Phase 1 — Continuity
Must prove:
- durable message append
- restart + resume correctness
- objective and next step resolution

### Phase 2 — Memory
Must prove:
- memory influences output
- memory relevance ranking works
- bad memory is filtered

### Phase 3 — Execution
Must prove:
- jobs persist across time
- jobs resume after interruption
- retries and repair loops work

### Phase 4 — Builder
Must prove:
- outputs are useful
- outputs are validated before use
- outputs are reusable

### Phase 5 — UI Truth
Must prove:
- UI reflects real system state
- no decorative panels
- approvals and jobs are real

### Phase 6 — Release Hardening
Must prove:
- clean install
- full scenario run
- rollback works
- evidence bundle exists

---

## Layer 3 — Product System

Phases 7–20 require real-world proof, not structural presence.

---

## Core Rule

Nexus is not 10/10 until behavior is proven, not described.
