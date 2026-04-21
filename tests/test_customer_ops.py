from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports, assert_nonempty_public_api


def test_customer_ops_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/customer_ops/__init__.py")
    assert_module_imports("nexus_os.customer_ops")
    assert_nonempty_public_api("nexus_os.customer_ops")


def test_customer_ops_behavior_contract() -> None:
    from nexus_os.customer_ops import process_event

    result = process_event("ticket_opened")

    assert result.event_type == "ticket_opened"
