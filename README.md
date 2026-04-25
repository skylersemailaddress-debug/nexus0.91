# Nexus v0.91

Nexus v0.91 is a unified AI operating system architecture and product shell. It combines one visible product shell, one core OS layer, one runtime/control plane, one registry, one event bus, one memory substrate, one mission model, one artifact model, one module contract, one operator surface model, and one rendered flagship client.

## Current release status

Current approved label: `CERTIFIED_BY_EVIDENCE`.

Current release truth is maintained in:

- `docs/release/CURRENT_STATUS.md`
- `docs/release/ENTERPRISE_BLOCKERS.md`
- `docs/ui/NEXUS_UI_MASTER_TRUTH.md`

The repo should not be judged from older launch-blocker language, archived phase plans, stale audit notes, or isolated documentation claims. Current authority order is:

1. GitHub CI on `main`
2. `scripts/run_enterprise_gate.py`
3. final certification output
4. validator outputs
5. issue closure matrix
6. active documentation

If a document contradicts current CI or gate evidence, it is stale and must be corrected or archived.

## Launch posture

Nexus v0.91 is in an evidence-certified green posture, not an unrestricted perfection claim. The repo may claim `CERTIFIED_BY_EVIDENCE` when current CI, enterprise gates, truth gates, and final certification remain green. It should not claim universal 10/10 commercial perfection without continuing product-substance audits.

## Product identity

Nexus is not a chatbot, generic copilot, dashboard, or model wrapper. It is a persistent adaptive synthetic intelligence and cognitive operating system intended to convert user intent into compounding forward progress through continuity, memory, planning, builder capability, execution, adaptive support, and truthful visibility.

The product north star is:

**Consistency of positive action toward what the user actually wants.**

It should optimize for consistency, recovery after drift, meaningful progress, clearer next action, reduced friction, follow-through, and compounding forward movement.

## UI doctrine

The flagship UI is governed by `docs/ui/NEXUS_UI_MASTER_TRUTH.md`.

Core UI truths:

- one workspace operating environment, not dashboard pages
- chat/composer is the primary command and reasoning surface
- mission, memory, module, proof, benchmark, and strategic views are summoned context surfaces
- operator control center is a summoned authority surface, not permanent panel clutter
- live state must back visible objectives, jobs, approvals, memory highlights, progress, readiness, and proof surfaces
- the UI must expose operational truth, not static product theater

## Runtime and product shell

Primary paths:

- Desktop shell: `./launch_nexus_desktop.sh`
- Textual shell: `./launch_nexus.sh`
- Installed command: `nexus`
- Developer mode: `nexus --developer` or `python -m nexus_os.ui --developer`
- Desktop API only: `python -m nexus_os.product.api_server --api-token <token>`

The standalone launchers are intentionally non-mutating. They expect an existing virtual environment with the project installed and, for desktop mode, existing dependencies under `desktop_shell/node_modules`.

## Architecture map

- `nexus_os/persistence`: durable persistence and atomic JSON snapshots
- `nexus_os/observability`: structured system health observability
- `nexus_os/shell`: workspace/composer shell canon
- `nexus_os/product`: standalone product and desktop API paths
- `nexus_os/ui`: rendered flagship client
- `nexus_os/intelligence`: capability routing, generation, validation, repair, self-extension
- `nexus_os/strategic`: strategic cognition, opportunity ranking, evidence-class deliberation
- `nexus_os/governance`: operator control, safeguards, release/readiness gates
- `nexus_os/core_os`: identity, policy, registry, mission state, event routing, memory routing
- `nexus_os/runtime`: run state machine, checkpoints, approvals, restore/replay, deterministic build/proof engine
- `nexus_os/module_fabric`: module contract validation and promotion
- `nexus_os/outputs`: internal vs standalone output routing
- `nexus_os/memory`: working, episodic, semantic, procedural, and reflective memory
- `nexus_os/operator`: canonical operator projection
- `nexus_os/models`: canonical data contracts
- `docs`: active doctrine, specs, release truth, and archive
- `tests`: deterministic validation suite

## Execution substrate

Canonical loop:

1. intake
2. plan
3. execute
4. validate
5. repair if needed
6. revalidate
7. complete or fail with evidence

The execution substrate supports run/job records, lifecycle states, retries, repair loops, validation evidence, event timelines, summaries, approvals, checkpoints, artifacts, and resumability.

Implementation-grade references:

- `docs/specs/NEXUS_EXECUTION_SUBSTRATE_SPEC.md`
- `docs/specs/NEXUS_AUTOBUILDER_SUBSTRATE_SPEC.md`

## Doctrine and specs

Primary doctrine/spec files:

- `docs/doctrine/NEXUS_DOCTRINE_0_91.md`
- `docs/doctrine/NEXUS_UI_DOCTRINE_0_91.md`
- `docs/doctrine/NEXUS_BEHAVIOR_AND_PSYCHOLOGY_DOCTRINE.md`
- `docs/doctrine/NEXUS_BUILDER_DOCTRINE.md`
- `docs/doctrine/NEXUS_MODE_INTELLIGENCE.md`
- `docs/doctrine/NEXUS_CORPORATE_MORPH_MODEL.md`
- `docs/doctrine/NEXUS_OPPORTUNITY_ENGINE.md`
- `docs/doctrine/NEXUS_UNIVERSAL_CONNECTOR_DOCTRINE.md`
- `docs/specs/NEXUS_0_91_MASTER_SPEC.md`
- `docs/specs/NEXUS_EXECUTION_SUBSTRATE_SPEC.md`
- `docs/specs/NEXUS_AUTOBUILDER_SUBSTRATE_SPEC.md`

These files are the constitutional product layer for Nexus v0.91 and beyond.

## Validation

Run:

```bash
python scripts/validate_docs_truth_hygiene.py
python scripts/validate_repo_truth_consistency.py
python scripts/run_enterprise_gate.py
python -m pytest
```

The enterprise gate covers continuity, memory/context integration, execution, UI truth, readiness, release hardening, security baseline, observability, adaptive learning, max-power scenarios, full-system wiring, final configuration, placeholder-test detection, repo truth consistency, master truth, final certification, and package/release manifest generation.

## Documentation hygiene

Historical or superseded docs belong under `docs/archive/`. Active docs must align with `CURRENT_STATUS.md` and the current validation chain. Cleanup should archive before deletion unless a file is an exact duplicate and has no live references.
