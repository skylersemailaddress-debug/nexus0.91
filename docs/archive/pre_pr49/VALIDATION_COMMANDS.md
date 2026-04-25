> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# VALIDATION COMMANDS

## Current Truth
Local validation is not release authority while GitHub CI is red.

## Currently Failing CI Areas
- master-completion-gate
- truth-gates
- enterprise-gate

## Known Failing/Misaligned Commands
- python scripts/validate_master_completion.py --check-git
- python -c "from nexus_os.governance.truth_gate import run_repo_truth_gates"

## Canonical Local Commands
Run these only as local prechecks:

```bash
python scripts/run_enterprise_gate.py
python scripts/security_baseline.py
python scripts/validate_nexus_enterprise.py
python scripts/run_release_hardening.py
python scripts/validate_release_hardening.py
python -m pytest -q tests
```

## Release Authority
A release is not ready until the canonical commands pass in GitHub Actions and all issue-closure evidence is reconciled.
