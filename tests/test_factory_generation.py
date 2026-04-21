from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports, assert_nonempty_public_api


def test_factory_generation_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/factory/__init__.py")
    assert_module_imports("nexus_os.factory")
    assert_nonempty_public_api("nexus_os.factory")


def test_factory_generation_behavior_contract() -> None:
    from nexus_os.factory import build_factory

    result = build_factory("core")

    assert result.name == "core"
