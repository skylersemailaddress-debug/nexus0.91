# Nexus v0.91 Post-Cleanup Stabilization Status

## Purpose

This status file reconciles the repo state after the documentation cleanup/archive pass and before any more feature work. It is intentionally a stabilization artifact, not a new product doctrine document.

## Connector-verified baseline

Current baseline inspected through GitHub connector:

- Repo: `skylersemailaddress-debug/nexus0.91`
- Baseline commit used for this stabilization branch: `b4eda582c894e32ebe4c601ab23271ecbb0d3925`
- Source commit: PR #54, `Archive stale release phase docs`
- Stabilization branch: `stabilize/post-cleanup-state-reconciliation`

## What is confirmed

### PR #54 is merged

PR #54 archived stale release phase documents and preserved full original content under `docs/archive/pre_pr49/`. The merge commit is `b4eda582c894e32ebe4c601ab23271ecbb0d3925`.

### Active release docs are clean by connector search

Connector search for active `NEXUS_PHASE_` docs under `docs/release` returned no results after the archive pass.

Expected active release layer:

- `docs/release/CURRENT_STATUS.md`
- `docs/release/ENTERPRISE_BLOCKERS.md`
- `docs/release/RELEASE_INDEX.md`
- `docs/release/evidence/`

### UI hover-native branch is not visible remotely through connector

Searches for the reported UI branch/work did not find a remote PR, branch, or commit:

- PR search: `hover-native OR ui/finish-hover-native-truth OR Implement hover-native UI truth primitives`
- Branch search: `ui`
- Commit search: `Implement hover-native UI truth primitives and validators`
- Code search: `ui_primitives HoverNativeUIState hover_native_ui`

Result: no connector-visible evidence that `ui/finish-hover-native-truth` is merged to `main` or pushed as a remote branch.

This does not prove the UI work does not exist locally. It means current remote `main` does not show it through the connector.

## Current likely state

The repo is not a single reconciled baseline yet.

Likely split state:

1. `main` includes PR #54 archive cleanup.
2. UI hover-native implementation may exist only locally or in a non-visible branch.
3. Audit branches exist and should be treated as diagnostic artifacts, not current product truth.
4. Codespaces/local workspace had stash/untracked-file noise during cleanup.
5. Some audit command failures may reflect branch/environment mismatch rather than final main truth.

## Do not do next

Do not start P0-1 live runtime scenario yet.

Do not start more features.

Do not run more broad audits from mixed branches.

Do not assume the reported UI implementation is on `main` until the branch or PR is visible and merged.

## Required stabilization sequence

### 1. Establish one product baseline

Use `main` after PR #54 as the truth baseline.

Commands to run locally when Codespaces is stable:

```bash
git checkout main
git pull origin main
git log --oneline -5
```

Confirm `b4eda582c894e32ebe4c601ab23271ecbb0d3925` or a later commit is present.

### 2. Recover or push UI hover-native branch

If the UI work exists locally, push it:

```bash
git branch --all | grep -i ui
git checkout ui/finish-hover-native-truth
git push origin ui/finish-hover-native-truth
```

If it exists under a different branch, identify it with:

```bash
git log --all --oneline --grep="hover-native"
git log --all --oneline --grep="UI truth primitives"
git log --all --oneline --grep="Implement hover-native"
```

Then open/reopen the PR and review it against `main`.

### 3. Merge UI branch only after validation

Minimum validation before merge:

```bash
PYTHONPATH=. python scripts/run_ui_truth_scenarios.py
PYTHONPATH=. python scripts/validate_ui_truth.py
PYTHONPATH=. python scripts/validate_docs_truth_hygiene.py
PYTHONPATH=. python scripts/validate_repo_truth_consistency.py
PYTHONPATH=. python -m pytest tests
PYTHONPATH=. python scripts/run_enterprise_gate.py
```

If commands require `PYTHONPATH=.`, record that as a baseline packaging issue rather than hiding it.

### 4. After UI merge, run one clean main validation

```bash
git checkout main
git pull origin main
python scripts/validate_docs_truth_hygiene.py
python scripts/validate_repo_truth_consistency.py
python scripts/run_ui_truth_scenarios.py
python scripts/validate_ui_truth.py
python -m pytest tests
python scripts/run_enterprise_gate.py
```

Only failures from this clean `main` run should be treated as current truth.

## Current blocker summary

| Blocker | Status | Meaning |
|---|---|---|
| Archive cleanup | Done on main via PR #54 | Repo docs are cleaner |
| UI hover-native implementation | Not connector-visible on remote | Must push/merge or disregard as local-only |
| Audit failures | Diagnostic | Need clean-main rerun after branch reconciliation |
| Baseline test health | Unknown from connector | Must rerun locally/CI |
| Next feature work | Paused | Do not start P0-1 yet |

## Final stabilization rule

The repo is stable only when there is one branch, preferably `main`, that contains:

- PR #54 archive cleanup
- any intended UI hover-native implementation
- generated evidence expected by validators
- passing docs truth hygiene
- passing repo truth consistency
- passing UI truth generation/validation
- a known pytest status
- a known enterprise gate status

Until then, the correct status is:

`STABILIZATION REQUIRED — BRANCH TRUTH FRAGMENTED`
