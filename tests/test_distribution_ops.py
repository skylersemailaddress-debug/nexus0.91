from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports


def test_distribution_ops_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/distribution_ops/__init__.py")
    assert_module_imports("nexus_os.distribution_ops")
