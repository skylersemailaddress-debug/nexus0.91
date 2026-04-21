from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports, assert_nonempty_public_api


def test_fleet_maintenance_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/fleet_maintenance/__init__.py")
    assert_module_imports("nexus_os.fleet_maintenance")
    assert_nonempty_public_api("nexus_os.fleet_maintenance")


def test_fleet_maintenance_behavior_contract() -> None:
    from nexus_os.fleet_maintenance import check_status

    result = check_status("asset-1")

    assert result.asset_id == "asset-1"
    assert result.status == "ok"
