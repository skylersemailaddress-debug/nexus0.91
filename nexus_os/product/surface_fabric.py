from __future__ import annotations

from typing import Any


def build_surface_manifests() -> dict[str, Any]:
    return {
        "ok": True,
        "surfaces": [
            {
                "id": "mission",
                "runtime_backed": True,
                "source_contract": "/projects/{project_id}/resume",
                "manifest": {
                    "fields": ["objective", "next_step"]
                }
            },
            {
                "id": "memory",
                "runtime_backed": True,
                "source_contract": "/memory/search",
                "manifest": {
                    "fields": ["selected_memories", "influence_trace"]
                }
            }
        ]
    }


def get_surface(surface_id: str) -> dict[str, Any] | None:
    data = build_surface_manifests()
    for s in data["surfaces"]:
        if s["id"] == surface_id:
            return s
    return None
