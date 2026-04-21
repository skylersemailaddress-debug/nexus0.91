from __future__ import annotations

from tests._proof_helpers import assert_file_exists, assert_module_imports, assert_nonempty_public_api


def test_benchmarking_module_exists_and_imports() -> None:
    assert_file_exists("nexus_os/benchmarking/__init__.py")
    assert_module_imports("nexus_os.benchmarking")
    assert_nonempty_public_api("nexus_os.benchmarking")


def test_benchmarking_behavior_contract() -> None:
    from nexus_os.benchmarking import run_benchmark

    result = run_benchmark(0.95)

    assert result.score == 0.95
