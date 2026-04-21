from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports, assert_nonempty_public_api


def test_distribution_ops_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/distribution/__init__.py")
    assert_module_imports("nexus_os.distribution")
    assert_nonempty_public_api("nexus_os.distribution")


def test_distribution_ops_behavior_contract() -> None:
    from nexus_os.distribution import create_plan

    result = create_plan("primary")

    assert result.name == "primary"
