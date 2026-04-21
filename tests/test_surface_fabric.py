from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports, assert_nonempty_public_api


def test_surface_fabric_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/surface_fabric/__init__.py")
    assert_module_imports("nexus_os.surface_fabric")
    assert_nonempty_public_api("nexus_os.surface_fabric")


def test_surface_fabric_behavior_contract() -> None:
    from nexus_os.surface_fabric import create_surface

    result = create_surface("main")

    assert result.name == "main"
