from __future__ import annotations

import json
from pathlib import Path


def _load(name: str) -> dict:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "release" / "evidence" / "execution" / f"{name}.json"
    return json.loads(target.read_text(encoding="utf-8"))


def test_artifact_lineage_integrity_contains_artifacts() -> None:
    data = _load("artifact_lineage_integrity")
    artifacts = data.get("artifacts", [])
    assert isinstance(artifacts, list)
    assert artifacts


def test_artifact_lineage_integrity_artifact_has_id() -> None:
    data = _load("artifact_lineage_integrity")
    artifacts = data.get("artifacts", [])
    assert artifacts[0].get("id")


def test_artifact_lineage_integrity_artifact_has_parent_field() -> None:
    data = _load("artifact_lineage_integrity")
    artifacts = data.get("artifacts", [])
    assert "parent" in artifacts[0]
