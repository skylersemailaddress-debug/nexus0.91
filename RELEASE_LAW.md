# Nexus Release Law

This repository is governed as a release-certification program, not an aspiration tracker.

## Completion law
Nothing is done until it is:
1. Implemented in runtime behavior
2. Exercised in a required scenario
3. Captured in an evidence artifact
4. Validated by a fail-closed validator
5. Reflected in release score eligibility

## Hard rules
1. Implemented but unproven = not done
2. Missing evidence = fail
3. Missing validator = fail
4. Overclaim = bug
5. Static UI for live operational claims = bug
6. Any open gate-blocker prevents score inflation
7. No manual enterprise-ready or 10/10 labels
8. No new roadmap replaces an open gate
9. Every merged PR must reference a closure ticket
10. Every closure ticket must change runtime behavior, proof, evidence, validator state, or release eligibility

## Ticket types
Only these ticket types count toward release closure:
- Implementation
- Proof
- Validator
- Downgrade

## Phase gate rule
No new phase may be claimed complete while its gate-blocker issues remain open.

## Release label rule
- Enterprise release ready requires all Gate A release milestones closed
- True 10/10 / max power requires all Gate A and Gate B milestones closed

## Downgrade rule
If a capability is not fully proven, it must be removed, hidden, or relabeled to its honest maturity state.

## Operating question for every ticket
What runtime behavior changed, what scenario proves it, what artifact records it, and what validator now passes because of it?
