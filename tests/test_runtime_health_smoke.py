from __future__ import annotations

from tests._proof_helpers import assert_module_imports


RUNTIME_MODULES = [
    "nexus_os.product.execution",
    "nexus_os.operator.market_projection",
    "nexus_os.operator.portfolio_projection",
    "nexus_observability.metrics",
    "nexus_security.runtime_enforcement",
]


def test_core_runtime_modules_import_cleanly() -> None:
    for module_name in RUNTIME_MODULES:
        assert_module_imports(module_name)
