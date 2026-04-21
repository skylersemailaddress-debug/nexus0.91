from pathlib import Path

def test_master_truth_doc_exists():
    assert Path("docs/specs/NEXUS_MASTER_TRUTH_AND_WORK_SYSTEM.md").exists()

def test_execution_checklist_exists():
    assert Path("docs/checklists/NEXUS_10_10_EXECUTION_CHECKLIST.md").exists()

def test_phase_gated_master_roadmap_exists():
    assert Path("docs/roadmaps/NEXUS_10_10_PHASE_GATED_MASTER_ROADMAP.md").exists()
