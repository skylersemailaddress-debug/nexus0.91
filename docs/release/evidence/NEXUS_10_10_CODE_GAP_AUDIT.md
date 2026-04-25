# Nexus v0.91 10/10 Code Gap Audit

## Executive verdict

Current credible label: `CERTIFIED_BY_EVIDENCE`.

Nexus v0.91 is in a cleaner and more credible repo state after the archive pass, but the code evidence still supports a bounded certification posture rather than an unrestricted commercial 10/10 claim. The enterprise gate is broad and materially useful, but several validators are still scenario/evidence driven rather than proof that the full app behaves as a polished end-user operating system under live messy use.

What is green:
- Release truth hierarchy is clean.
- Stale phase docs are archived.
- Enterprise gate orchestrates continuity, memory, execution, UI truth, readiness, hardening, security, observability, adaptive learning, final configuration, placeholder detection, master truth, 10/10 gate, final certification, pytest, and release manifest generation.
- UI truth projection validator exists and checks evidence/runtime-source equality for required scenarios.

What is not yet proven as commercial 10/10:
- Full live runtime behavior under messy input.
- Hover-native ambient UI implementation, beyond docs/projection evidence.
- Full desktop launch smoothness and user onboarding.
- Production-grade authz/audit/tenant boundaries.
- Builder/product-company/autonomous product operation as fully implemented runtime behavior.
- Validators that make fake/stub implementations impossible across all domains.

Top blockers:
1. UI implementation proof: current UI truth validator checks projection evidence, not full hover-native interaction behavior.
2. Runtime live-path proof: enterprise gate is broad, but live runtime endpoint execution is not proven by this audit.
3. Commercial launch polish: install, first-run, desktop child-process management, and recovery need direct proof.
4. Memory influence depth: must prove memory causally changes planning/execution with inspectable traces.
5. Builder/product-company scope: must remain bounded until runtime build/repair/package/portfolio behavior is proven.
6. Governance depth: actor attribution, audit logs, tenant boundaries, fail-closed policy, and secret handling need production-grade proof.
7. Observability depth: traces must reconstruct decisions, failures, memory influence, approvals, policy, artifacts, and UI state.
8. Validator semantic depth: existence/shape checks must be upgraded where still shallow.
9. Persistence durability: crash/restart/backup/restore/corruption recovery must be proven.
10. End-to-end acceptance: messy goal -> run/jobs -> approval -> repair -> artifact -> validation -> UI truth -> restart -> evidence must pass as a single app-level scenario.

## Evidence basis

Inspected or used as evidence:
- `README.md`
- `docs/release/CURRENT_STATUS.md`
- `docs/release/ENTERPRISE_BLOCKERS.md`
- `docs/release/RELEASE_INDEX.md`
- `docs/ui/NEXUS_UI_MASTER_TRUTH.md`
- `scripts/run_enterprise_gate.py`
- `scripts/validate_ui_truth.py`
- `scripts/run_ui_truth_scenarios.py`
- `scripts/validate_repo_truth_consistency.py`
- `scripts/validate_docs_truth_hygiene.py`
- repository search results for active release phase docs after archive pass
- prior PR #54 archive-pass state

Note: this audit was produced through the GitHub connector. It is code-grounded but not a substitute for running the full test suite locally/CI.

## Domain scorecard

| Domain | Current score | Evidence | Main gap | Priority |
|---|---:|---|---|---|
| Runtime and execution | 7 | Enterprise gate runs execution scenario and validation scripts | live messy-goal execution not proven here | P0 |
| Continuity and resume | 7 | Enterprise gate runs continuity scenarios and validators | restart realism and objective/next-step depth need live proof | P0 |
| Message persistence | 6 | Covered by continuity intent, but not directly verified in this audit | durable append/replay path needs direct proof | P0 |
| Memory influence | 7 | Gate runs memory context, trace, behavior, and memory validators | causal influence under real planning/execution needs deeper proof | P1 |
| Run/job lifecycle | 7 | Execution scenario/validator paths exist | full pause/resume/repair/revalidate lineage must be live-proven | P0 |
| Approval/policy hooks | 6.5 | UI truth and execution scenarios include approval concepts | production approval gates and audit need deeper proof | P0 |
| Artifact lineage/evidence | 7 | release evidence and manifest generation exist | artifact provenance across real runs needs end-to-end proof | P1 |
| UI implementation | 6 | UI truth docs and projection validator exist | hover-native interaction primitives not proven | P0 |
| Desktop shell/launch | 5.5 | launchers are documented | first-run reliability and desktop recovery need proof | P1 |
| Product API completeness | 6 | product API exists by README claim; not deeply inspected here | canonical UI state endpoints need verification | P0 |
| Builder/module generation | 6.5 | enterprise gate includes max-power/full-system checks | useful builder repair/package path needs product-level proof | P1 |
| Opportunity/product-company | 5 | bounded roadmap/spec posture | not a current autonomous product-company claim | P2 |
| Governance/authz/audit | 6.5 | security baseline and governance validators run | production-grade policy/audit/tenant proof needed | P0 |
| Observability/traces | 7 | observability validator in enterprise gate | reconstructability under failures needs live proof | P1 |
| Persistence/recovery | 6.5 | continuity/release hardening validators exist | crash/backup/restore/corruption tests need proof | P0 |
| Validators/test depth | 7 | enterprise gate is broad | some validators may still be shape/evidence checks | P0 |
| Install/onboarding | 5.5 | launch docs exist | commercial first-run flow not proven | P1 |
| Product polish/docs | 7.5 | README/release docs now clean | user/operator guides and troubleshooting need runtime alignment | P2 |

## Domain details

### Runtime and execution

Current evidence:
- `scripts/run_enterprise_gate.py` runs `run_execution_scenarios.py`, `validate_execution.py`, and `validate_execution_resume.py`.

Implemented:
- There is at least a release-gated execution scenario path.
- Execution is part of the core enterprise gate.

Thin/scaffolded:
- This audit did not prove the execution path handles messy user goals through a live product runtime.

Missing:
- Single end-to-end runtime proof from user intent through jobs, repairs, artifacts, validation, and UI truth.

Required tickets:
- Add live end-to-end execution scenario using canonical product entrypoint.
- Prove pause/resume/retry/repair/revalidate from persisted state.
- Prove artifact lineage emitted from real run/job records.

Acceptance tests:
- `python scripts/run_execution_scenarios.py`
- `python scripts/validate_execution.py`
- `python scripts/validate_execution_resume.py`
- new app-level end-to-end scenario.

Files likely touched:
- `nexus_os/runtime/`
- `nexus_os/product/`
- `scripts/run_execution_scenarios.py`
- `tests/test_execution_*`

### Continuity and resume

Current evidence:
- Enterprise gate runs `run_continuity_scenarios.py` and `validate_continuity.py`.

Implemented:
- Continuity is release-gated.

Thin/scaffolded:
- Live restart behavior through actual product shell/API was not proven by this audit.

Missing:
- Proof that objective, next step, blockers, approvals, active run, and artifacts restore after process restart.

Required tickets:
- Add live restart/resume scenario across product entrypoint.
- Add objective/next-step restoration tests from durable state.

Acceptance tests:
- restart app mid-run, resume exact state, verify UI/API projection.

Files likely touched:
- `nexus_os/persistence/`
- `nexus_os/product/`
- `nexus_os/shell/`
- `tests/test_continuity_*`

### Message persistence

Current evidence:
- Continuity gate implies message/state persistence coverage, but this audit did not inspect a durable append implementation.

Implemented:
- Unknown from connector-level audit.

Thin/scaffolded:
- If message append only stores summaries or shallow state, continuity remains incomplete.

Missing:
- Direct durable append/replay proof.

Required tickets:
- Verify and harden message append path.
- Add replay-based continuity test.

Acceptance tests:
- append messages, restart, replay/build context, verify ordering/actors/meta.

Files likely touched:
- `nexus_os/persistence/`
- `nexus_os/shell/`
- `nexus_os/product/`

### Memory retrieval and influence

Current evidence:
- Enterprise gate runs memory context, trace, behavior, and general memory validators.

Implemented:
- Memory has multiple gate categories, which is stronger than simple existence.

Thin/scaffolded:
- Need proof that memory causally changes real planning/execution, not just generated evidence dictionaries.

Missing:
- Same-input/different-memory live behavior proof.
- Operator-visible influence traces tied to decisions.

Required tickets:
- Add memory causal-influence scenario through actual planner/execution path.
- Add negative tests for stale/contradictory memory.

Acceptance tests:
- same prompt with different memory state causes justified different next step and trace.

Files likely touched:
- `nexus_os/memory/`
- `nexus_os/product/`
- `scripts/run_memory_behavior_scenarios.py`
- `tests/test_memory_*`

### UI implementation against master truth

Current evidence:
- `scripts/validate_ui_truth.py` requires evidence files and checks surface/runtime equality for mission, approvals, progress, memory, and proof.
- UI docs define hover-native ambient command OS.

Implemented:
- UI truth projection validation exists.
- Evidence-driven UI truth checks exist.

Thin/scaffolded:
- Validator does not prove hover-native edge reveal, bottom command rail, pin-anything, adaptive opening state, keyboard parity, local hover tools, explain-why, undo/recovery, or no-dashboard interaction behavior.

Missing:
- Actual interaction-level UI primitive tests and evidence.

Required tickets:
- Implement UI primitive model and state builder.
- Add interaction evidence files for hover reveal, command rail, pinning, adaptive state, keyboard parity, explain-why, no-dashboard regression.
- Upgrade `validate_ui_truth.py` to validate those evidence files.

Acceptance tests:
- `python scripts/run_ui_truth_scenarios.py`
- `python scripts/validate_ui_truth.py`
- `pytest tests/test_ui_*`

Files likely touched:
- `nexus_os/product/ui_truth.py`
- `nexus_os/product/ui_state.py`
- `nexus_os/ui/`
- `desktop_shell/`
- `scripts/run_ui_truth_scenarios.py`
- `scripts/validate_ui_truth.py`

### Desktop shell and launch reliability

Current evidence:
- README documents `launch_nexus_desktop.sh` and desktop API path.

Implemented:
- Desktop path exists by repo documentation.

Thin/scaffolded:
- This audit did not prove fresh install, dependency detection, API child-process recovery, crash recovery, logs, or update path.

Missing:
- Commercial first-run and degraded-mode proof.

Required tickets:
- Add desktop launch smoke test.
- Add API unavailable/degraded UI behavior.
- Add dependency diagnostics.

Acceptance tests:
- fresh clone setup; desktop launches; API failure handled; logs emitted.

Files likely touched:
- `desktop_shell/`
- `launch_nexus_desktop.sh`
- `nexus_os/product/api_server.py`

### Product API completeness

Current evidence:
- README describes desktop API and product runtime.

Implemented:
- Product API path exists by documentation.

Thin/scaffolded:
- Exact endpoint completeness not verified in this audit.

Missing:
- Canonical UI state endpoint if not already present.
- Endpoint coverage for resume, messages, memory, runs/jobs, approvals, artifacts, proof, health, diagnostics.

Required tickets:
- Add API endpoint inventory test.
- Add UI state endpoint contract.

Acceptance tests:
- UI can render from canonical API state only.

Files likely touched:
- `nexus_os/product/api_server.py`
- `nexus_os/product/desktop_runtime.py`
- `tests/test_product_api_*`

### Builder / module generation / repair / validation

Current evidence:
- Enterprise gate includes max-power and full-system wiring validators.

Implemented:
- Builder direction appears represented in repo architecture and gate categories.

Thin/scaffolded:
- Need proof that builder produces useful working artifacts with repair and packaging.

Missing:
- Messy input -> generated tool -> validation failure -> repair -> package -> proof scenario.

Required tickets:
- Add builder artifact end-to-end scenario.
- Add negative repair test.

Acceptance tests:
- generated artifact runs and passes validation after repair loop.

Files likely touched:
- `nexus_os/intelligence/`
- `nexus_os/module_fabric/`
- `nexus_os/outputs/`
- `tests/test_builder_*`

### Opportunity engine / product-company capability

Current evidence:
- Product-company spec is bounded roadmap, not current autonomous claim.

Implemented:
- Direction exists.

Thin/scaffolded:
- Product-company capability should remain non-overclaimed.

Missing:
- Market intelligence, portfolio, economics, distribution, customer ops, maintenance burden, benchmarking as runtime-backed capabilities.

Required tickets:
- Keep bounded label until runtime behavior exists.
- Add portfolio/economics models and tests only when implemented.

Acceptance tests:
- opportunity ranking produces traceable scores and maintenance/economic state.

Priority:
- P2; not required for bounded launch but required for broad 10/10 product-company claims.

### Governance, permissions, authz, audit logs

Current evidence:
- Enterprise gate runs `security_baseline.py` and governance-related validators.

Implemented:
- Security baseline exists.

Thin/scaffolded:
- Production-grade tenancy, authz, actor attribution, and policy audit depth need direct proof.

Missing:
- Fail-closed unsafe action tests.
- Actor-linked audit trail for approvals/policy/execution.
- Secret-handling negative tests.

Required tickets:
- Add policy/audit event model tests.
- Add authorization boundary tests.

Acceptance tests:
- unsafe action fails closed, emits audit event, is visible to operator.

Files likely touched:
- `nexus_os/governance/`
- `nexus_os/models/`
- `tests/test_security_*`

### Observability and trace reconstruction

Current evidence:
- Enterprise gate runs `validate_observability.py`.

Implemented:
- Observability is included in release gate.

Thin/scaffolded:
- Need direct failure reconstruction across real run/job/memory/approval chains.

Missing:
- Unified trace correlation from output to memory, run, approval, policy, artifact, and UI projection.

Required tickets:
- Add trace ID propagation.
- Add failure reconstruction scenario.

Acceptance tests:
- for any artifact/output, reconstruct cause, memory influence, run/job, approval, validation evidence.

### Persistence, migrations, backup/restore, corruption recovery

Current evidence:
- Continuity and release hardening validators exist in enterprise gate.

Implemented:
- Persistence is part of architecture and validation posture.

Thin/scaffolded:
- Backup/restore, migration, crash recovery, and corruption handling need explicit proof.

Missing:
- Schema/version migration tests.
- Backup/restore and corruption recovery scenario.

Required tickets:
- Add persistence recovery test suite.
- Add versioned state migration proof.

### Validators and test depth

Current evidence:
- Enterprise gate is comprehensive and includes pytest.
- `validate_ui_truth.py` is a concrete example of evidence checking.

Implemented:
- Strong gate orchestration exists.

Thin/scaffolded:
- Some validators may be synthetic evidence or contract-shape validators.

Missing:
- Meta-validator that classifies validators by semantic depth.
- Negative tests proving fake implementations fail.

Required tickets:
- Add validator depth audit.
- Add negative fixtures for each major domain.

Acceptance tests:
- fake/stub implementation cannot pass enterprise gate.

### Install/onboarding/release packaging

Current evidence:
- README lists launch paths and validation commands.

Implemented:
- Launch commands are documented.

Thin/scaffolded:
- Fresh install and first-run flow not proven here.

Missing:
- One-command setup, env diagnostics, dependency check, onboarding project, reset/uninstall path.

Required tickets:
- Add install smoke test and first-run guide generated from real commands.
- Add desktop dependency validator.

## 10/10 scenario acceptance test

Complete scenario:
1. User gives messy multi-step goal.
2. Nexus creates objective and stateful mission.
3. Relevant memory is retrieved, ranked, and traced.
4. Nexus creates real run/jobs.
5. Execution proceeds and records transitions.
6. Risky step pauses for approval.
7. User approves; execution resumes.
8. Failure occurs; Nexus repairs and revalidates.
9. Artifact is produced with lineage.
10. Validator evidence is emitted.
11. UI shows calm hover-native state, with relevant work only when useful or pinned.
12. Explain-why shows memory/runtime/evidence reasons.
13. App restarts.
14. Resume returns exact objective, run state, approval history, artifact, next step, and evidence.
15. Operator can reconstruct all decisions through traces.

Current pass/fail/unknown map:
- Objective/continuity: partially proven by gate, live end-to-end unknown.
- Memory influence: partially proven by memory validators, live causal depth unknown.
- Run/job execution: partially proven by execution validators, live messy path unknown.
- Approval: partially proven by scenarios, production governance depth unknown.
- Artifact/evidence: partially proven, full lineage unknown.
- UI truth: projection equality proven, hover-native implementation unknown/incomplete.
- Restart/resume: validator-covered, full app restart proof unknown.
- Trace reconstruction: observability validator exists, full chain proof unknown.

## Build order

P0-1: Live end-to-end runtime scenario
- Files: `scripts/run_full_system_wiring_scenarios.py`, `nexus_os/product/`, `tests/`
- Acceptance: messy goal completes through run/jobs, approval, artifact, validation, resume.
- Validation: `python scripts/run_full_system_wiring_scenarios.py && python scripts/validate_full_system_wiring.py`

P0-2: UI hover-native implementation proof
- Files: `nexus_os/product/ui_state.py`, `nexus_os/ui/`, `desktop_shell/`, `scripts/run_ui_truth_scenarios.py`, `scripts/validate_ui_truth.py`
- Acceptance: edge reveal, command rail, pin-anything, adaptive opening, keyboard parity, explain-why evidence.
- Validation: `python scripts/run_ui_truth_scenarios.py && python scripts/validate_ui_truth.py && pytest tests/test_ui_*`

P0-3: Runtime persistence/restart proof
- Files: `nexus_os/persistence/`, `nexus_os/runtime/`, `nexus_os/product/`, `tests/test_continuity_*`
- Acceptance: restart preserves objective, next step, run/job, approval, artifact.
- Validation: `python scripts/run_continuity_scenarios.py && python scripts/validate_continuity.py`

P0-4: Governance/audit fail-closed proof
- Files: `nexus_os/governance/`, `tests/test_security_*`
- Acceptance: unsafe action blocked, attributed, logged, recoverable.
- Validation: `python scripts/security_baseline.py`

P0-5: Validator semantic-depth hardening
- Files: `scripts/validate_*`, `tests/negative/`
- Acceptance: fake/stub implementations fail.
- Validation: `python scripts/validate_no_placeholder_tests.py && python scripts/validate_enterprise_gate_coverage.py`

P1-1: Desktop commercial launch smoke test
- Files: `launch_nexus_desktop.sh`, `desktop_shell/`, `nexus_os/product/api_server.py`
- Acceptance: fresh install boot, API child process recovery, clear diagnostics.
- Validation: new desktop smoke script.

P1-2: Memory causal behavior proof
- Files: `nexus_os/memory/`, `nexus_os/product/`, `scripts/run_memory_behavior_scenarios.py`
- Acceptance: same input/different memory yields justified behavior change with trace.
- Validation: `python scripts/run_memory_behavior_scenarios.py && python scripts/validate_memory_behavior.py`

P1-3: Observability reconstruction chain
- Files: `nexus_os/observability/`, runtime models, tests.
- Acceptance: output can be traced to run, memory, approval, policy, artifact, evidence.
- Validation: `python scripts/validate_observability.py`

P1-4: Builder repair/package proof
- Files: `nexus_os/intelligence/`, `nexus_os/module_fabric/`, `nexus_os/outputs/`
- Acceptance: generated artifact validates, repairs, revalidates, packages.
- Validation: builder scenario script/test.

P2-1: Product-company runtime model
- Files: `nexus_os/models/product.py`, portfolio/economics modules.
- Acceptance: bounded portfolio/economic state and operator projection.
- Validation: product-company scenario tests.

P2-2: User/operator docs from real launch flow
- Files: `docs/`, launch scripts.
- Acceptance: docs match actual commands and failure modes.
- Validation: install smoke test.

## No-overclaim guard

Current allowed claim:
- Nexus v0.91 is `CERTIFIED_BY_EVIDENCE` when main CI, enterprise gate, final certification, validator outputs, and release evidence are green.

Do not claim yet:
- universal 10/10 commercial perfection.
- fully autonomous product-company operation.
- fully implemented hover-native UI unless interaction primitives and validators pass.
- production enterprise tenant/security posture unless actor attribution, authz, audit, fail-closed policy, and secret handling are proven.
- live runtime execution of messy goals unless app-level end-to-end scenario passes.

## Commands run for this audit

Not run through connector:
- `python scripts/validate_docs_truth_hygiene.py`
- `python scripts/validate_repo_truth_consistency.py`
- `python -m pytest tests`

Reason: GitHub connector can edit and inspect repository files but does not execute the repository test suite. Run these in CI/Codespace before merge.
