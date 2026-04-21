from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports, assert_nonempty_public_api


def test_portfolio_engine_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/portfolio/__init__.py")
    assert_module_imports("nexus_os.portfolio")
    assert_nonempty_public_api("nexus_os.portfolio")


def test_portfolio_engine_behavior_contract() -> None:
    from nexus_os.portfolio import build_portfolio

    result = build_portfolio(["a", "b"])

    assert result.items == ["a", "b"]
