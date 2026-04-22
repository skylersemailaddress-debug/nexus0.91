from __future__ import annotations

from typing import List, Dict, Any
import uuid

SIGNALS: List[Dict[str, Any]] = []


def ingest_signal(title: str, source: str, weight: float = 1.0) -> dict:
    item = {
        "id": str(uuid.uuid4()),
        "title": title,
        "source": source,
        "weight": weight,
    }
    SIGNALS.append(item)
    return item


def rank_opportunities() -> dict:
    scored = []

    for s in SIGNALS:
        score = float(s.get("weight", 1.0))
        scored.append({
            "id": s["id"],
            "title": s["title"],
            "score": score,
            "reasons": [f"source:{s['source']}", f"weight:{score}"],
            "source_count": 1,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return {
        "ok": True,
        "signals_ingested": len(SIGNALS),
        "opportunities": scored,
    }
