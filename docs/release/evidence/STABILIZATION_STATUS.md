# Stabilization Status

## Import baseline reconciliation (2026-04-25)

- Baseline is `origin/main` at commit `b4eda58`.
- PR #54 archive cleanup is present in this baseline.
- Script import baseline is fixed (`scripts/_repo_bootstrap.py` + script bootstrap imports).
- Required commands pass without `PYTHONPATH=.` from repo root:
  - `python scripts/run_ui_truth_scenarios.py`
  - `python scripts/validate_ui_truth.py`
  - `python scripts/validate_docs_truth_hygiene.py`
  - `python scripts/validate_repo_truth_consistency.py`
  - `python scripts/run_enterprise_gate.py`
  - `python -m pytest tests`
- UI hover-native work is missing on this baseline.

**Status:** BASELINE CLEAN / UI WORK MISSING.

**Next action:** rerun P0-2 hover-native UI implementation after this branch is merged.
