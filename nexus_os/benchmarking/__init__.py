from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkResult:
    score: float
    label: str
    gaps: list[str]


def run_benchmark(score: float) -> BenchmarkResult:
    if score >= 0.8:
        return BenchmarkResult(score, "excellent", [])
    if score >= 0.6:
        return BenchmarkResult(score, "good", ["optimize_performance"])
    if score >= 0.4:
        return BenchmarkResult(score, "weak", ["improve_quality", "reduce_errors"])
    return BenchmarkResult(score, "poor", ["major_rework_required"])


__all__ = ["BenchmarkResult", "run_benchmark"]
