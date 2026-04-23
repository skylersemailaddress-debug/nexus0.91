from __future__ import annotations

from pathlib import Path

import tomllib


REQUIRED_PROJECT_SCRIPTS = {"nexus", "nexus-ui"}


def test_pyproject_has_build_system_and_project_metadata() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))

    build_system = data.get("build-system", {})
    assert build_system.get("build-backend") == "setuptools.build_meta"
    assert isinstance(build_system.get("requires"), list)
    assert build_system["requires"]

    project = data.get("project", {})
    assert project.get("name")
    assert project.get("version")
    assert project.get("requires-python")


def test_console_entrypoints_exist_in_pyproject() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})

    missing = sorted(REQUIRED_PROJECT_SCRIPTS.difference(set(scripts.keys())))
    assert not missing, f"Missing required console scripts: {missing}"
