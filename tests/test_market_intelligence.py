from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports


def test_market_intelligence_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/market_intelligence/__init__.py")
    assert_module_imports("nexus_os.market_intelligence")
