from __future__ import annotations

import json
from pathlib import Path


def _load(name: str) -> dict:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "release" / "evidence" / "execution" / f"{name}.json"
    return json.loads(target.read_text(encoding="utf-8"))


def test_fail_repair_revalidate_has_revalidated_job() -> None:
    data = _load("fail_repair_revalidate")
    jobs = data.get("jobs", [])
    assert jobs
    assert jobs[0].get("status") == "revalidated"


def test_fail_repair_revalidate_has_recovered_run() -> None:
    data = _load("fail_repair_revalidate")
    run = data.get("run", {})
    assert run.get("status") == "recovered"


def test_fail_repair_revalidate_has_reasoning() -> None:
    data = _load("fail_repair_revalidate")
    reasoning = data.get("reasoning", [])
    assert isinstance(reasoning, list)
    assert reasoning
