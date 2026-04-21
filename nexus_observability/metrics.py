from __future__ import annotations

from collections import Counter


class MetricsRegistry:
    def __init__(self) -> None:
        self._counters: Counter[str] = Counter()

    def increment(self, name: str, amount: int = 1) -> None:
        self._counters[name] += amount

    def snapshot(self) -> dict[str, int]:
        return dict(self._counters)


def default_metrics() -> MetricsRegistry:
    registry = MetricsRegistry()
    registry.increment("process.starts", 0)
    registry.increment("process.successes", 0)
    registry.increment("process.failures", 0)
    return registry
