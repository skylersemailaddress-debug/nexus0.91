# NEXUS Definition of Done

NEXUS is only considered finished when all of the following are true:

- Build passes
- Tests pass
- Runtime checks pass
- Release checks pass
- Evidence bundle exists
- Rollback artifact/path exists
- Security checks pass
- Documentation matches reality

## Locked validation path
- python -m pytest tests -q
- python scripts/run_enterprise_gate.py
- python scripts/security_baseline.py
