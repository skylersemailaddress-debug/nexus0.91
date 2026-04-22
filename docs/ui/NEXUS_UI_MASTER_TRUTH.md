# NEXUS UI MASTER TRUTH
## Canonical UI doctrine for Nexus0.91

Status: canonical
Authority: highest UI truth
Applies to: all Nexus product surfaces, desktop shell, web shell, product launcher, UI-facing docs, demos, and release claims

---

## 1. Purpose

Nexus is not a dashboard-first product and not a chat-only product.

Nexus is a living operating workspace for intelligence, execution, memory, approvals, and artifacts.

The UI must make Nexus feel:
- calm
- predictive
- tool-powerful
- deeply personal
- operationally truthful
- ahead of the user without fighting the user

The UI must never degrade into:
- static dashboard clutter
- fake operational chrome
- decorative control surfaces
- chat as the only visible mode of capability
- pane-heavy enterprise SaaS bloat

---

## 2. Core identity

Nexus UI is a:

**hover-native ambient command OS**

This means:
- the workspace is primary
- controls are present but mostly hidden
- the system reveals itself on intent
- the user can pin anything
- the system can adapt the workspace by user, mode, and urgency
- the UI should feel almost empty at rest and fully powerful in motion

---

## 3. Non-negotiable UI laws

### Law 1 - Workspace primacy
The canvas is sacred.
No persistent chrome should reduce the feeling of open workspace unless the user pins it or active work requires it.

### Law 2 - Hover-native reveal
Primary control surfaces are hover-reveal by default:
- top
- left
- right
- bottom
- local inline hover tools

### Law 3 - Pin-anything control
Any reveal surface may be:
- temporary
- soft pinned
- hard pinned

### Law 4 - Chat is primary control, not permanent visual occupation
The chat bar is the persistent primary command method, but it is hover-native by default and should recede when active work takes over.

### Law 5 - Default open state is curated, never generic
On open, Nexus should present a curated readiness field based on:
- active work
- what changed
- predicted intent
- user habits
- urgency
- time/context rhythm

### Law 6 - No static pane may survive without live utility
Nothing stays on screen without purpose.
Every visible pane must either:
- advance work
- support a decision
- reveal system truth
- reduce friction
- protect against risk

### Law 7 - Operational truth over visual comfort
The UI must reflect live state.
No demo-only, decorative, stale, or unbacked system surface is allowed in a release-ready Nexus UI.

### Law 8 - Tool-first interaction
The interface must be useful as a tool, not just beautiful as a surface.
Every surfaced object should provide meaningful actions.

### Law 9 - Heavy keyboard parity
Every major hover-native interaction must also be available through keyboard and command palette control.

### Law 10 - Personalization is part of product truth
The UI must adapt to the user over time in behavior, density, reveal patterns, prioritization, and quick actions.

---

## 4. Canonical resting state

At rest, the UI should feel:
- almost empty
- premium
- calm
- prepared

Visible by default should be minimal:
- clean workspace
- subtle ambient status or readiness signal
- adaptive opening content if relevant
- no heavy shell chrome

The UI should never open as a dead blank void unless the product explicitly determines that nothing should be surfaced.

---

## 5. Canonical edge model

### Left edge
Purpose:
- continuity
- navigation
- threads
- projects
- rituals
- history
- memory anchors

Default behavior:
- hover-reveal
- pinnable
- adaptive strength based on usage

### Right edge
Purpose:
- active work
- jobs/runs
- approvals
- blockers
- prepared outputs
- recommendations
- runtime/system truth

Default behavior:
- hover-reveal
- urgency-sensitive
- slightly more assertive under active execution states

### Top edge
Purpose:
- global control
- mode
- workspace identity
- notifications
- command palette trigger
- account/system state
- connected systems

Default behavior:
- hover-reveal
- compact
- keyboard-equivalent

### Bottom edge
Purpose:
- command
- input
- quick actions
- attachments
- voice
- suggested commands
- recent command memory

Default behavior:
- hover-reveal
- expands when active
- recedes after submit and active work begins

---

## 6. Canonical chat bar behavior

The chat bar is the primary command surface.

### Requirements
- hover-reveal from bottom edge by default
- smooth slide-up on approach
- expandable during input
- recedes after work begins
- can be pinned if user prefers permanence
- supports attachments, voice, quick actions, and command recall
- auto-scrolls downward appropriately after send
- supports strong keyboard-first reopening
- never permanently consumes workspace unless pinned or active

### Disallowed
- permanently large bottom composer with no adaptive behavior
- chat occupying visual dominance after work output takes over
- dead or hidden command state without quick reopen affordance

---

## 7. Canonical opening panes

The default opening field must be adaptive, not fixed, but may draw from these pane families:

- Now
- What Changed
- In Motion
- Needs You
- Prepared For You
- Context

These are not permanent dashboard modules.
They are adaptive operational reveals.

### Now
Current objective, top change, and best next move.

### What Changed
What completed, failed, moved, or now needs attention since the user last engaged.

### In Motion
Live runs, jobs, progress, retries, blockers.

### Needs You
Approvals, conflicts, decisions, review requests.

### Prepared For You
Likely next commands, staged drafts, likely needed artifacts, recommended actions.

### Context
Memory or state highlights affecting current decisions.

---

## 8. Quick action toolbar truth

Nexus must provide an adaptive quick action toolbar.

### Requirements
- hover-revealed by default
- context-aware
- user-adaptive
- pinnable
- includes likely next actions, favorite tools, recent actions, and mode-relevant actions
- includes hover-reveal settings and customization affordances

### Must support
- action reorder
- tool visibility control
- pin/unpin
- shortcut assignment
- density modes
- adaptive behavior toggles

---

## 9. Local hover toolbars

Hover-native interaction is not limited to edges.

When the user hovers on inline objects, Nexus should surface local, context-relevant micro-tools.

### Examples
Text:
- rewrite
- summarize
- compare
- expand
- convert to plan

Artifacts:
- inspect
- branch
- approve
- export
- annotate

Jobs:
- retry
- pause
- inspect logs
- escalate
- approve

The UI must favor local relevance over persistent clutter.

---

## 10. Keyboard doctrine

Nexus must be heavy on keyboard shortcuts and fully customizable.

### Requirements
- command palette as first-class control layer
- all major hover surfaces accessible by keyboard
- customizable global shortcuts
- customizable mode-specific shortcuts
- pin/unpin via keyboard
- move between panes via keyboard
- open/close chat via keyboard
- open/close rails via keyboard
- customizable shortcut profile storage

Keyboard interaction is not optional polish. It is core product truth.

---

## 11. Mode system

The UI must be mode-sensitive.
At minimum, Nexus should support adaptive behavior for modes such as:
- focus
- build
- review
- inspect
- decide
- war-room
- autopilot/background

The UI should reweight:
- pane priority
- reveal behavior
- quick actions
- proactive surfacing
- density
- interruption style

---

## 12. Personalization truth

Nexus must learn and adapt to:
- common tasks
- preferred density
- favorite tools
- preferred pinned surfaces
- edge usage habits
- likely next actions
- preferred shortcut patterns
- work rhythms by time and context
- tolerance for proactive surfacing

The UI should become more individually tuned over time.

---

## 13. Calmness rules

Hover-native systems can become noisy. Nexus must remain calm.

### Must do
- use hover thresholds
- avoid accidental reveal spam
- suppress reveals during focused typing/editing unless explicitly requested
- use smooth motion
- avoid covering critical content abruptly
- only escalate on genuine urgency or strong confidence

### Must not do
- twitch
- flicker
- interrupt constantly
- magnetize every panel equally
- create the feeling of unstable UI chrome

---

## 14. Trust and explainability

Nexus must allow the user to understand why something was surfaced.

The user should be able to inspect:
- why this pane is here
- why this action is recommended
- why this memory matters
- what Nexus is doing in background
- what is blocked
- what changed

A psychic UI without explainability becomes creepy or untrustworthy.

---

## 15. Undo, branching, and recovery

If Nexus performs meaningful work, the UI must support:
- undo
- revert
- branch
- compare versions
- restore prior state/checkpoint

This is part of operational trust.

---

## 16. Density and ritual support

The UI must support:
- density presets
- ritual launch states
- workspace snapshots
- restore-last-layout
- per-mode pin presets
- quiet mode
- operator mode

Users should be able to make Nexus more minimal or more operational without breaking doctrine.

---

## 17. Anti-patterns

The following are explicitly disallowed as release truth:

- static dashboard-first UI
- always-visible pane walls by default
- chat occupying the screen after active work begins
- decorative status cards not backed by live state
- hidden system activity with no inspectability
- mouse-only reveal mechanics
- fixed generic home screen for all users
- non-pinnable adaptive surfaces
- personalization claims without actual adaptive behavior
- operational surfaces that cannot be validated against runtime truth

---

## 18. Validation standard

The UI can only be described as compliant with master truth if:

- hover-native edge behavior exists for primary surfaces
- pinning exists for reveal surfaces
- chat bar follows hover/recede doctrine
- opening state is curated/adaptive
- keyboard parity exists for major surfaces
- quick actions are adaptive and customizable
- local hover tools exist or are intentionally scoped with documented rationale
- release-facing docs do not claim static dashboard behavior as canonical
- no UI claim exceeds implemented truth

---

## 19. Canonical doctrine statement

Nexus UI is a calm, predictive, hover-native living workspace.
The canvas stays clean.
Controls reveal on intent.
The system curates what matters.
Anything can be pinned.
Keyboard is first-class.
Operational truth is visible when needed and absent when not.
The UI should feel one step ahead of the user without getting in the user’s way.

---

## 20. Final release label rule

A Nexus UI release may only be labeled:
- `MASTER_TRUTH_ALIGNED`

if the validation gate confirms that the shipped UI and docs align with this file.

Otherwise it must be labeled with a bounded status such as:
- `PARTIAL_ALIGNMENT`
- `BOUNDED_PROTOTYPE`
- `DOCTRINE_AHEAD_OF_IMPLEMENTATION`
