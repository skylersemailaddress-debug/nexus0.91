from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FactorySpec:
    name: str


def build_factory(name: str) -> FactorySpec:
    return FactorySpec(name=name)
