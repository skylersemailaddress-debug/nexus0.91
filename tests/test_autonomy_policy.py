from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports, assert_nonempty_public_api


def test_autonomy_policy_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/autonomy_policy/__init__.py")
    assert_module_imports("nexus_os.autonomy_policy")
    assert_nonempty_public_api("nexus_os.autonomy_policy")


def test_autonomy_policy_behavior_contract() -> None:
    from nexus_os.autonomy_policy import evaluate

    result = evaluate("deploy")

    assert result.allowed is True
