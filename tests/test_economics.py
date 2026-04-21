from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports, assert_nonempty_public_api


def test_economics_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/economics/__init__.py")
    assert_module_imports("nexus_os.economics")
    assert_nonempty_public_api("nexus_os.economics")


def test_economics_behavior_contract() -> None:
    from nexus_os.models.economics import EconomicsRecord

    result = EconomicsRecord(revenue=10.0, cost=4.0)

    assert result.profit() == 6.0
