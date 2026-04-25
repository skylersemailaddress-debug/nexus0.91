> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# NEXUS TRUTH CONSTITUTION

## Core Rule

Nexus is 10/10 only when every visible behavior, decision, and output is correct, durable, state-backed, adaptive where required, auditable, recoverable, and proven under real runtime execution, with no gap between claim and observed behavior.

If any required section fails, Nexus is not 10/10.

No partial credit. No overclaim. No doctrine-only completion.

## 1. System Truth

Must be true:
- all state is durable and reload-safe
- restart preserves continuity
- no silent loss across messages, runs, memory, approvals, artifacts, and operator-visible state
- hidden transient state does not change outcomes without being inspectable

Fails if:
- anything resets unexpectedly
- resume is shallow or partial
- state loss is possible without detection
- hidden state influences behavior without traceability

## 2. Continuity

Must be true:
- exact objective resumes
- exact trajectory resumes
- next step is deterministic and state-derived
- resume surfaces are consistent with underlying state

Fails if:
- conversation effectively restarts
- next step is generic, guessed, or inconsistent
- resume omits important blockers, approvals, or artifacts

## 3. Memory

Must be true:
- memory changes decisions and outputs
- memory is ranked, filtered, explainable, suppressible, and bounded by relevance
- memory influence is inspectable by operators where appropriate

Required proof:
- same input
- different memory state
- different justified output

Fails if:
- memory is stored but ignored
- irrelevant memory leaks into decisions
- memory influence cannot be explained

## 4. Execution

Must be true:
- system starts work, persists work, pauses/resumes, retries, repairs, and produces artifacts
- execution survives interruption and restart
- execution state is reflected in run/job records and summaries

Fails if:
- system mainly talks about work
- execution is simulated
- execution is not state-backed
- artifacts are not bound to real execution lineage

## 5. Approvals and Control

Must be true:
- approvals block execution when required
- approvals persist
- approvals are auditable and actor-linked
- approvals and intervention points are surfaced truthfully

Fails if:
- approvals are cosmetic
- actions bypass approval state
- actor identity or audit trail is missing

## 6. UI Truth

Must be true:
- every UI element reflects real runtime state
- irrelevant surfaces collapse or disappear when not needed
- UI is workspace-first, adaptive, collapsible, and state-driven
- composer/chat may exist, but may not be the sole operational truth surface once live state exists

Fails if:
- static fake panels exist
- placeholders or decorative operational surfaces remain
- UI shows claims not backed by state
- UI doctrine exceeds implementation truth

## 7. Readiness

Must be true:
- system surfaces what matters now
- system surfaces what changed
- system surfaces what needs action
- system surfaces what is likely next
- ranking is explainable and materially correct

Fails if:
- important items are buried
- ordering appears random or unjustified
- readiness cannot explain why items are ranked as shown

## 8. Adaptive Learning

Required for full 10/10 Final Nexus:
- system adapts based on user actions, outcomes, and behavior over time
- reinforcement and decay exist and are safe
- learning improves future behavior without overfitting or destabilization

Fails if:
- no meaningful improvement occurs over time
- system overfits or gets stuck in early patterns
- adaptation cannot be bounded or explained

## 9. Behavioral Proof

Must be true:
- all required scenarios pass against real runtime, not mocks
- evidence is emitted for each required scenario class

Required scenario classes:
- continuity after restart
- memory alters decision
- execution survives interruption
- approval blocks flow
- UI reflects real state
- readiness ranks correctly

## 10. Release Hardening

Must be true:
- clean install works
- boot works without manual fixes
- CI passes
- rollback works
- evidence bundle exists

Fails if:
- setup is fragile
- validation depends on environment hacks
- release claims exceed emitted evidence

## 11. No Overclaim

Must be true:
- nothing is described above what is proven
- labels and release statements match current evidence state

Fails if:
- docs exceed reality
- UI doctrine exceeds implementation
- features are claimed but not validated
- maturity label exceeds proof state

## 12. Enterprise Standard

Must be true:
- deterministic where required
- observable
- auditable
- recoverable
- no hidden state
- no silent failure

Fails if:
- failure states are not surfaced
- important transitions cannot be reconstructed
- recovery paths are absent or misleading

## 13. Security and Governance

Must be true:
- authenticated actors where required
- permissioned actions
- policy-gated risky execution
- auditable action history
- no privileged hidden paths

Fails if:
- actions lack attribution
- policy is bypassable
- approvals lack actor identity
- governance surfaces do not reflect real enforcement

## 14. Observability

Must be true:
- state transitions are inspectable
- run/job history is traceable
- failures are visible
- ranking reasons are inspectable
- memory influence is inspectable

Fails if:
- important failures are silent
- operator cannot reconstruct why the system acted
- evidence cannot be traced back to the originating state transition
