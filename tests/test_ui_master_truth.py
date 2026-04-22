from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ui_master_truth_exists() -> None:
    assert (ROOT / "docs" / "ui" / "NEXUS_UI_MASTER_TRUTH.md").exists()


def test_ui_doctrine_exists() -> None:
    assert (ROOT / "docs" / "ui" / "NEXUS_UI_DOCTRINE.md").exists()


def test_master_truth_terms() -> None:
    text = (ROOT / "docs" / "ui" / "NEXUS_UI_MASTER_TRUTH.md").read_text(encoding="utf-8").lower()
    required = [
        "hover-native",
        "chat bar",
        "quick action",
        "keyboard",
        "workspace",
    ]
    missing = [term for term in required if term not in text]
    assert not missing, f"Missing UI master truth terms: {missing}"
