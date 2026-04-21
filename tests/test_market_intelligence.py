from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports, assert_nonempty_public_api


def test_market_intelligence_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/market_intelligence/__init__.py")
    assert_module_imports("nexus_os.market_intelligence")
    assert_nonempty_public_api("nexus_os.market_intelligence")


def test_market_intelligence_behavior_contract() -> None:
    from nexus_os.market_intelligence import analyze_signal

    result = analyze_signal("sensor", "test signal", 0.5)

    assert result.source == "sensor"
    assert result.summary == "test signal"
    assert result.score == 0.5
