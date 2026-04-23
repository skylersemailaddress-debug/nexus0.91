from __future__ import annotations

import importlib


def test_nexus_entrypoint_target_imports() -> None:
    module = importlib.import_module("nexus_os.product.launcher")
    assert hasattr(module, "main")


def test_nexus_ui_entrypoint_target_imports() -> None:
    module = importlib.import_module("nexus_os.ui.__main__")
    assert hasattr(module, "main")
