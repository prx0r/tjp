"""BRP + TradeScore — runnable form of docs/eli5.md. All factors 0..1 except gaps >= 0."""
from __future__ import annotations


def brp(v: float, i: float, w: float, l: float, q: float, e: float, s: float) -> float:
    e = max(e, 1e-6)
    s = max(s, 1e-6)
    return round((v * i * w * l * q) / (e * s), 3)


def trade_score(brp_value: float, valuation_gap: float, reflexivity: float, catalyst: float) -> float:
    return round(brp_value * valuation_gap * reflexivity * catalyst, 3)


def scarcity_rent(value_unlocked: float, unit_cost: float, time_to_supply: float, substitution_ease: float) -> float:
    return round((value_unlocked / max(unit_cost, 1e-6)) * (time_to_supply / max(substitution_ease, 1e-6)), 3)
