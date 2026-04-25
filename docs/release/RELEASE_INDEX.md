# Release Documentation Index

This directory is the active release-truth layer for Nexus v0.91.

## Current release truth

- `CURRENT_STATUS.md` — current green/evidence-certified release status and source-of-truth order
- `ENTERPRISE_BLOCKERS.md` — current blocker posture and remaining non-blocking hardening track
- `evidence/` — generated release, validator, and certification evidence

## UI authority

The canonical UI authority is outside this directory:

- `docs/ui/NEXUS_UI_MASTER_TRUTH.md`

## Historical material

Historical phase plans, superseded blocker narratives, old audit notes, and pre-certification release posture belong under:

- `docs/archive/pre_pr49/`

Archived files are retained for traceability but must not override current CI, enterprise gate, validator, or certification evidence.

## Rule

If a release document contradicts current CI, `scripts/run_enterprise_gate.py`, validator output, final certification output, or `CURRENT_STATUS.md`, the document is stale and must be corrected or archived.
