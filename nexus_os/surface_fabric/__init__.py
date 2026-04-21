from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Surface:
    name: str


def create_surface(name: str) -> Surface:
    return Surface(name=name)
