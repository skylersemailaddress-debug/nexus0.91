from __future__ import annotations

import importlib
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def assert_module_imports(module_name: str) -> None:
    module = importlib.import_module(module_name)
    assert module is not None


def assert_file_exists(rel_path: str) -> None:
    path = repo_root() / rel_path
    assert path.exists(), f"Missing required path: {rel_path}"


def assert_nonempty_public_api(module_name: str) -> None:
    module = importlib.import_module(module_name)
    public = [name for name in dir(module) if not name.startswith("_")]
    assert public, f"{module_name} has no public API"
