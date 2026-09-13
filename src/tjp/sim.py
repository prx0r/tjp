"""Cohort builder — uses canonical IDs from ids.py only. No duplicate maps."""
from __future__ import annotations
import json
from pathlib import Path
from .ids import SAFE_ASSET_MAP

BASE = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade"


def cohort(universe: list = None, listings: list = None) -> dict:
    uni_raw = universe if universe is not None else json.load(open(BASE / "universe.json"))["markets"]
    ls = listings if listings is not None else json.load(open(BASE / "listings.json"))
    uni = {m["id"].lower(): m for m in uni_raw}

    rows = []
    for l in ls:
        asset = l["asset"]
        project = SAFE_ASSET_MAP.get(asset.upper(), asset.lower())
        old_id = asset.lower() + "usdt"
        new_id = project + "usdt"
        m = uni.get(old_id) or uni.get(new_id) or {}
        state = m.get("state") if m else None
        lifecycle = "ACTIVE" if state == "enabled" else "DISABLED" if state else "UNKNOWN"
        rows.append({
            "project": project,
            "asset": asset,
            "announced": l.get("announced", ""),
            "market": m.get("id", ""),
            "lifecycle": lifecycle,
            "market_created": (m.get("created_at") or "")[:10],
        })
    active = sum(1 for r in rows if r["lifecycle"] == "ACTIVE")
    disabled = sum(1 for r in rows if r["lifecycle"] == "DISABLED")
    return {"n": len(rows), "active": active, "disabled": disabled,
            "unknown": len(rows) - active - disabled,
            "rows": rows}
