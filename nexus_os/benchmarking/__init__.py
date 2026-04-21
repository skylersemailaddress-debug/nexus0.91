from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    score: float


def run_benchmark(score: float) -> BenchmarkResult:
    return BenchmarkResult(score=score)
