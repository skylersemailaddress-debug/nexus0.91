# Nexus v0.9

Nexus v0.9 is a unified AI operating system architecture with:

- one visible product shell
- one core OS layer
- one runtime/control plane
- one registry
- one event bus
- one memory substrate
- one mission model
- one artifact model
- one module contract
- one operator surface model
- one rendered flagship client

This repository implements one coherent system, not donor-seamed wrappers.

Nexus v0.9 is not a chatbot, not a copilot, not a dashboard, and not a generic model wrapper. It is being evolved into a **persistent adaptive synthetic intelligence** that should feel like a second cognitive processor: an AI chip in the mind, a second mind, and a synthetic executive operating system for personal and organizational action.

This repository therefore has two truths that must be held together simultaneously:

1. **Architecture truth** — the repo already contains serious kernel, runtime, governance, memory, shell, and UI foundations.
2. **Product doctrine truth** — Nexus is a live second-mind system whose job is to turn user intent into compounding forward progress through continuity, memory, planning, builder capability, execution, adaptive support, and truthful visibility.

The product must never drift into shallow “assistant” framing. The architecture must never drift into disconnected control-plane infrastructure without product identity.

---

## Canonical Direction

- Nexus 0.5: shell and interaction canon
- Nexus intelligence kernel: absorbed deterministic planning/build/proof/self-extension patterns
- NexusV3: runtime/control-plane donor patterns

Result in this repo: one integrated Nexus v0.9 architecture.

Nexus v0.9 is the transition release where Nexus stops feeling like an AI interface and starts behaving like a stateful operating system with dependable execution. Enterprise release evidence is maintained in docs/release and gates these claims.

---

## Product Identity

Nexus is intended to become:
- a persistent adaptive synthetic intelligence
- a second mind
- a synthetic executive operating system
- a cognitive operating system
- a personal and organizational intelligence substrate
- an outcome engine that converts intent into finished work over time

It should feel like:
- my second mind is here
- it remembers what matters
- it has already been working
- it already knows what matters now
- it can build, execute, and adapt over time

The chat surface is the anchor. The real product is the live intelligence behind it.

---

## North Star

The north star of Nexus is:

**Consistency of positive action toward what the user actually wants.**

Nexus should not optimize for:
- time in app
- stimulation
- hollow productivity theater
- engagement for its own sake

It should optimize for:
- consistency
- recovery after drift
- meaningful progress
- clearer next action
- reduced friction
- follow-through
- barriers automated away
- forward movement that compounds over time

Permanent emotional truths of the system include:
- progress over perfection
- 2 steps forward and 1 step back is still forward
- 1 percent better more than 50 percent of days is a win
- setbacks are information, not identity failure
- failed attempts are useful evidence
- re-entry is success

The system must be positive, grounded, non-manipulative, non-shaming, and realistic.
It must never become a guilt machine, pseudo-therapy engine, or hype product.

---

## Product Doctrine Highlights

Nexus doctrine is now defined in the doctrine files under `docs/doctrine/`.

Core doctrine areas include:
- product identity and core operating constitution
- UI doctrine for a live cognitive surface
- behavior and psychology doctrine
- Builder doctrine
- adaptive mode intelligence doctrine
- corporate morph model
- opportunity engine doctrine

The governing doctrine file is:
- `docs/doctrine/NEXUS_DOCTRINE_0_91.md`

Key system truths include:
- chat/composer remains the permanent center
- everything else should be dynamic, relevance-driven, state-derived, summoned, and inspectable
- Builder must be one of the strongest parts of Nexus
- Nexus should infer what mode of intelligence the user needs rather than forcing persona selection
- the system should learn the user’s thinking style, strengths, weaknesses, drift patterns, and leverage points
- the system should remove friction and automate around weaknesses
- the system should discover and pursue opportunities, especially monetizable AI opportunities, through an Opportunity Engine
- the system should scale upward into founder/team/company operation through mandate packs rather than separate products

---

## Flagship UI Doctrine (Nexus 0.5 Canon)

- One workspace operating environment, not dashboard pages.
- Chat/composer is the primary surface for command, reasoning, and mission framing.
- Mission, memory, module, proof, benchmark, and strategic views are summoned context surfaces.
- Operator control center is available as a summoned authority surface, not permanent panel clutter.
- Motion and interaction language are calm, high-trust, and focus-preserving.
- Information hierarchy is explicit: primary, secondary, summoned, background, operator-only.

This shell direction remains correct.

For Nexus 0.9, the shell must become truthful:
- live state must back the surfaces
- objectives, jobs, approvals, memory highlights, and progress must be real
- the interface should answer what matters now, what Nexus is doing, what changed, and what the next best move is
- the experience should feel like the exposed surface of an active synthetic mind, not a static SaaS dashboard

---

## Rendered Client

- `nexus_os/ui` provides a real rendered Textual client (not contract-only) that consumes:
	- `nexus_os/shell/session.py` and `nexus_os/shell/surface.py` for workspace/composer shell contracts
	- `nexus_os/operator/surface_model.py` and `nexus_os/models/operator.py` for operator projections
	- live `NexusOS` mission/runtime/registry/memory/artifact state for mission and release surfaces
- Primary launch path (standalone product mode): `./launch_nexus.sh`
- Installed launch path: `nexus` (standalone product mode)
- Developer-heavy launch path: `nexus --developer` or `python -m nexus_os.ui --developer`
- Summoned rendered surfaces include approvals, memory, modules, proofs/release, strategy, opportunities, governance, and world/self model views.

The standalone launcher is intentionally non-mutating. It expects an existing virtual environment with the project already installed into that environment.

---

## Desktop-First Product Shell

- Primary commercial shell path is desktop-first and standalone: `./launch_nexus_desktop.sh`
- The desktop shell is web-rendered and native-hosted via Electron under `desktop_shell/`
- The shell consumes the real Nexus runtime through `nexus_os.product.api_server` and `nexus_os.product.desktop_runtime`
- Conversation/composer remains the primary workspace surface; models/governance/proof depth is summoned on demand
- Textual remains available as fallback/admin/operator shell from the desktop app (`Operator Shell`) or via `./launch_nexus.sh`

Quick start:

```bash
./launch_nexus_desktop.sh
```

The launcher is intentionally non-mutating. It expects an existing virtual environment with the project installed and existing desktop dependencies under `desktop_shell/node_modules`.

Run the desktop API only:

```bash
python -m nexus_os.product.api_server --api-token <token>
```

State and mutation endpoints require a bearer token. The Electron shell provisions one automatically for its child API process.

---

## Standalone Product Mode

- Product mode is the default user experience: conversation-first, minimal clutter, contextual depth.
- Main chat stays concise and user-forward by default.
- Technical/proof/operator depth is available on demand through summoned surfaces (`/proof`, `/governance`, `/module`, `/memory`, `/council`).
- Sidebar and technical panes are not forced on users in product mode, but remain available.

This must continue to evolve toward a premium live cognitive surface rather than a feature-dense dashboard.

---

## Conversational Intelligence Layer

- `nexus_os/shell/conversation_layer.py` adds a dedicated turn-handling layer above shell/runtime stack.
- It owns conversational turn routing, response composition, context framing, and mode transitions between:
	- conversation and clarification
	- strategic inspection
	- mission launch/resume
	- contextual technical surface routing
- Natural language can launch mission work directly; command support remains available and first-class.

This layer must eventually reflect adaptive mode intelligence, need-state inference, memory-grounded context, and execution-aware response shaping.

---

## Adaptive Tone and Memory Continuity

- Conversation output is adapted using bounded operational affective signals (load, friction, execution/recovery mode).
- Tone is calibrated for support utility (`minimal_and_structured`, `direct_and_goal_focused`, or concise support modes), not anthropomorphic personality scripting.
- Conversation continuity persists across sessions through conversation history snapshots and memory writes into working/episodic/semantic/reflective strata.
- Main chat surfaces only high-value summaries by default; deep internals remain contextual and user-requested.

Nexus doctrine now extends this further:
- tone must remain positive, grounded, realistic, non-manipulative, and non-shaming
- re-entry must be easy
- progress must be preserved psychologically and operationally
- memory must shape behavior, not just be stored

---

## What Nexus 0.9 Must Prove

Nexus 0.9 is the first believable stateful execution release.

It must prove:
- continuity works reliably
- memory affects behavior and context
- state resolves into action
- resume is a real system snapshot
- execution can persist across time
- approvals and intervention points are real
- Builder can create useful capabilities
- opportunities can be surfaced and acted on
- the UI reflects live operational truth, not static shell mocks

A real 0.9 should pass this scenario:
1. user gives Nexus a multi-step goal
2. Nexus stores it durably
3. objective and next step resolve
4. relevant memory is retrieved
5. a run/job begins
6. execution progresses over time
7. approvals and blockers are visible
8. the user returns later and sees real progress, pending approvals, and next actions

If runtime evidence shows Nexus still mostly chats instead of executing mission flows, the enterprise gate must fail for v0.9.

---

## Structure

- `nexus_os/persistence`: durable persistence layer (atomic JSON snapshots, NexusStateSerializer, PersistenceHealth) — opt-in, bounded to single-node FS
- `nexus_os/observability`: structured system health observability (SystemHealthSnapshot across missions, modules, runtime, artifacts, strategic, persistence — operator-facing, surfaced in projection)
- `nexus_os/shell`: Nexus shell canon (chat/composer-first, summoned surfaces)
- `nexus_os/shell/conversation_layer.py`: product conversation routing layer for turn handling, continuity, and contextual surface separation
- `nexus_os/ui`: rendered flagship client consuming shell/operator contracts
- `nexus_os/product`: standalone launcher path (`python -m nexus_os.product`, `nexus`)
- `nexus_os/intelligence`: native intelligence kernel (capability routing, create/compose/refuse policy, spec/IR/generation, validation/proof/readiness, repair, self-extension)
- `nexus_os/strategic`: evidence-driven strategic cognition layer (world/self/user models, strategic evidence ingestion, machine-readable opportunity ranking, evidence-class council deliberation, calibrated synthesis uncertainty, bounded proactivity, affective effectiveness loop, governed self-improvement)
- `nexus_os/governance`: operator control, constitutional safeguards, trust lifecycle governance, release/readiness bundles, CI truth gates
- `nexus_os/governance/security.py`: tenancy-ready boundary model and authz/security posture contract
- `nexus_os/core_os`: identity, policy, registry, mission state, event routing, memory routing
- `nexus_os/runtime`: run state machine, checkpoints, approvals, restore/replay, deterministic build/proof engine
- `nexus_os/module_fabric`: module contract validation and promotion logic
- `nexus_os/outputs`: internal vs standalone output routing and proof semantics
- `nexus_os/memory`: unified memory substrate (working, episodic, semantic, procedural, reflective)
- `nexus_os/operator`: canonical operator surface projection
- `nexus_os/models`: canonical data contracts
- `docs`: architecture, operator model, unification map, doctrine, and specs
- `tests`: deterministic architecture validation suite

This structure should increasingly be interpreted through the doctrine/spec lens, not just as technical modules.

---

## Execution Substrate Direction

Nexus must include a real execution substrate.

The canonical execution loop is:
- intake
- plan
- execute
- validate
- repair if needed
- revalidate
- complete or fail with evidence

The execution substrate should support:
- run or job records
- lifecycle states
- retries
- repair loops
- validation evidence
- event timelines
- summaries
- approvals / policy hooks
- checkpoints
- artifacts
- resumability

These patterns are informed by the Autobuilder truth set, but are integrated into Nexus as a subsystem, not as the full product identity.

See:
- `docs/specs/NEXUS_EXECUTION_SUBSTRATE_SPEC.md`
- `docs/specs/NEXUS_AUTOBUILDER_SUBSTRATE_SPEC.md`

---

## Builder Direction

Builder is one of the strongest parts of Nexus.

It exists so the system can:
- detect capability gaps
- create tools the user needs
- scaffold workflows
- build automations
- create internal capabilities
- build marketable product artifacts
- patch and maintain what it created

Builder is not a side utility.
It is how Nexus creates leverage and avoids dead ends.

See:
- `docs/doctrine/NEXUS_BUILDER_DOCTRINE.md`

---

## Opportunity Engine Direction

For founder and leverage-seeking use cases, Nexus includes an Opportunity Engine.

This subsystem should:
- discover
- rank
- simulate
- select
- build
- deploy
- measure
- maintain
- reallocate

opportunities, especially around AI tools, automations, systems, and monetizable products.

See:
- `docs/doctrine/NEXUS_OPPORTUNITY_ENGINE.md`

---

## Corporate Morph Direction

Nexus must scale from:
- individual
- founder
- team
- company
- enterprise

It should scale through mandate packs, role specialization, shared org memory, workflow ownership, approvals, and governance rather than becoming a separate product.

See:
- `docs/doctrine/NEXUS_CORPORATE_MORPH_MODEL.md`

---

## Documentation Layers

The repository now has distinct documentation layers:

### Doctrine Layer
Defines identity, behavior, UI law, builder doctrine, adaptive mode doctrine, opportunity doctrine, and corporate morph doctrine.

### Spec Layer
Defines implementation-grade system behavior for:
- Nexus 0.91 as a product
- execution substrate
- Autobuilder-derived substrate integration

### Architecture Truth
Documents what is currently real in the codebase and how the system is currently structured.

All future work should preserve alignment across these three layers.

---

## Validation

Run:

```bash
python -m pytest
```

The test suite validates:

- unified registry behavior
- unified mission model
- canonical capability routing and create/compose/refuse behavior
- strategic world/self modeling with live strategic evidence ingestion from mission/runtime/trust/operator signals
- machine-readable opportunity ranking using strategic fit, expected value, feasibility, risk, confidence, user alignment, reuse leverage, and weakness coupling
- evidence-class aware think-tank deliberation with bounded rounds/participants and calibrated uncertainty reasons
- bounded initiative policy and operational affective adaptation with effectiveness feedback loops
- operator control center, trust lifecycle visibility, restore/replay confidence, and release/readiness governance
- shell doctrine enforcement (workspace-first, composer-first, summoned-surface model)
- flagship operator projection sections for mission control, module fabric, memory, strategy, and governance
- rendered UI structural/flow coverage for shell boot, navigation, summoned surfaces, mission/operator commands, strategic/governance surfaces
- mandatory policy enforcement holds and bypass resistance paths
- structured mutation planning with machine-readable invariants
- replay/restore integrity verification and corruption detection
- weighted trust evidence promotion/demotion signals
- repo truth gates and package/release verification workflow
- native module generation and standalone output separation
- validation/proof/readiness and mutation safety integration
- unified artifact model
- typed event bus behavior
- module contract integrity
- internal vs standalone output routing
- deterministic runtime/build/proof flow
- documentation truth alignment

As Nexus moves toward 0.9 truth, additional validation should increasingly cover:
- continuity correctness
- memory-influenced context build
- objective / next-step resolution
- run/job persistence
- approval pause/resume correctness
- summary and resume completeness
- Builder usefulness
- UI truthfulness against live state

---

## Bounded Maturity

- `first_class` is reserved for well-proven core paths.
- `bounded_prototype` is used for real but explicitly constrained subsystems.
- `experimental` and `structural_only` remain non-overclaimed and operator-visible.
- Rendered client is terminal-native (Textual), not a browser SPA; visual and interaction behavior is real and test-covered, while web deployment remains intentionally bounded.
- Security posture is bounded but explicit: workspace-scoped tenancy boundary, operator-governed authz boundary, and no-secrets-in-mission-contracts policy model.

Nexus should remain honest about maturity. The doctrine does not justify overclaiming. It defines where the system is going and what must become true for 0.9 and 1.0 to be credible.

---

## Source of Truth Files

Primary doctrine / spec files:
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

These files are now the constitutional product layer for Nexus v0.9 and beyond.