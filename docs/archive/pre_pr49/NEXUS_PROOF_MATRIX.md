> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# NEXUS PROOF MATRIX

This file defines required proof scenarios for each constitution section.

## Continuity
- scenario: restart_active_mission
- validator: validate_continuity.py
- evidence: evidence/continuity/restart_active_mission.json
- pass: objective, next step, approvals, and artifacts preserved

## Memory
- scenario: same_input_different_memory
- validator: validate_memory_influence.py
- evidence: evidence/memory/memory_influence.json
- pass: output differs with justified reasoning

## Execution
- scenario: interrupt_and_resume_run
- validator: validate_execution_resume.py
- evidence: evidence/execution/resume_run.json
- pass: run resumes and completes

## Approvals
- scenario: approval_blocks_execution
- validator: validate_approval_gate.py
- evidence: evidence/approvals/block.json
- pass: execution halted until approval

## UI Truth
- scenario: ui_reflects_runtime_state
- validator: validate_ui_truth.py
- evidence: evidence/ui/runtime_binding.json
- pass: all surfaces map to real state

## Readiness
- scenario: readiness_ranking_correctness
- validator: validate_readiness.py
- evidence: evidence/readiness/ranking.json
- pass: high-priority items surfaced correctly

## Release
- scenario: clean_install_and_boot
- validator: validate_release.py
- evidence: evidence/release/install.json
- pass: system installs and boots cleanly
