from pathlib import Path

def test_nexus_10_10_master_roadmap_exists():
    assert Path("docs/roadmaps/NEXUS_10_10_MASTER_ROADMAP.md").exists()

def test_nexus_10_10_master_checklist_exists():
    assert Path("docs/checklists/NEXUS_10_10_MASTER_CHECKLIST.md").exists()
