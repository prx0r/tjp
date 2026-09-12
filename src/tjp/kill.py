"""Kill detector — runnable form of docs/eli5kill.md. Own high SR + rising SR, exit on flip."""
from __future__ import annotations

LIFECYCLE = ["DISCOVERY", "SHORTAGE", "RENT", "RESPONSE", "PEAK", "HEALING", "COLLAPSE"]


def kill_score(new_supply: float, inventory: float, lead_fall: float, substitution: float,
               buyer_roi_fall: float, demand_fall: float) -> float:
    """Each input 0..1 (strength of that kill signal). Higher = closer to exit."""
    return round((new_supply + inventory + lead_fall + substitution + buyer_roi_fall + demand_fall) / 6, 3)


def derivative_warnings(series: dict) -> list:
    """series: factor -> oldest..latest list. Returns triggered warnings."""
    out = []
    d = series.get("demand_growth", [])
    if len(d) >= 3 and d[-1] < d[-2] < d[-3]:
        out.append("demand decelerating 3 periods")
    u = series.get("utilization", [])
    if len(u) >= 3 and u[-1] < u[-2] < 100 <= u[-3]:
        out.append("utilization rolling from 100")
    lt = series.get("lead_time", [])
    if len(lt) >= 3 and lt[-1] < lt[-2] < lt[-3]:
        out.append("lead times shortening — exit warning even if price rising")
    inv = series.get("inventory", [])
    if len(inv) >= 3 and inv[-1] > inv[-2] > inv[-3]:
        out.append("persistent inventory rebuild")
    return out


def lifecycle_stage(util_trend: str, inv_trend: str, lead_trend: str, price_trend: str, capacity_trend: str) -> str:
    if inv_trend == "up" and lead_trend == "down":
        return "HEALING"
    if price_trend == "up" and capacity_trend == "up_up" and util_trend != "up":
        return "PEAK"
    if price_trend == "up" and inv_trend == "down" and lead_trend == "up":
        return "RENT"
    if util_trend == "up" and inv_trend == "down":
        return "SHORTAGE"
    if price_trend == "down" and inv_trend == "up":
        return "COLLAPSE"
    return "DISCOVERY"
