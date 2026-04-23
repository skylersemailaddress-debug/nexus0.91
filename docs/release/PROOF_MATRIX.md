# Nexus Proof Matrix

Every capability must map to scenario, evidence, and validator.

Continuity -> restart_active_mission -> continuity_report.json -> validate_continuity.py
Memory -> same_input_different_memory -> memory_report.json -> validate_memory.py
Execution -> interrupt_and_resume_run -> execution_report.json -> validate_execution.py
Approvals -> approval_blocks_execution -> approvals_report.json -> validate_approvals.py
UI -> ui_reflects_runtime_state -> ui_report.json -> validate_ui_truth.py
Readiness -> readiness_ranking_correctness -> readiness_report.json -> validate_readiness.py
Release -> clean_install_boot_rollback -> release_report.json -> validate_release.py

Rule: Missing proof fails the gate.
