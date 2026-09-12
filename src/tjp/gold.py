"""GOLD scoring — literal implementation of docs/agichat.md weights."""
from __future__ import annotations

WEIGHTS = {
    "scarcity_migration": 20,
    "valuation_convexity": 20,
    "catalyst_proximity": 15,
    "reflexivity": 15,
    "liquidity_access": 10,
    "narrative_compression": 10,
    "falsifiability": 10,
}


def score(factors: dict) -> dict:
    total = 0.0
    parts = {}
    for k, w in WEIGHTS.items():
        v = max(0.0, min(1.0, float(factors.get(k, 0.0))))
        parts[k] = round(v * w, 1)
        total += v * w
    total = round(total, 1)
    band = "GOLD" if total >= 85 else ("READY" if total >= 75 else ("WATCH" if total >= 60 else "RESEARCH"))
    return {"total": total, "band": band, "parts": parts}
