from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports


def test_surface_fabric_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/surface_fabric/__init__.py")
    assert_module_imports("nexus_os.surface_fabric")
