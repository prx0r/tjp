"""Cohort builder — uses canonical IDs, not ticker prefix matching."""
from __future__ import annotations
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade"
SIZE = 1000.0


def cohort(universe: list = None, listings: list = None) -> dict:
    uni_raw = universe if universe is not None else json.load(open(BASE / "universe.json"))["markets"]
    ls = listings if listings is not None else json.load(open(BASE / "listings.json"))
    uni = {m["id"].lower(): m for m in uni_raw}

    # Canonical asset → project mapping (no prefix matching)
    CANONICAL = {
        "QUAN": "quantus", "QUANTUS": "quantus",
        "PRL": "pearl", "PEARL": "pearl",
        "TSC": "tensorcash", "NOID": "paranoid", "CNX": "crynux",
        "MDL": "modelos", "CSD": "computesubstrate",
    }

    rows = []
    for l in ls:
        asset = l["asset"]
        project = CANONICAL.get(asset.upper(), asset.lower())
        # Look up by both old and new market IDs
        old_id = asset.lower() + "usdt"
        new_id = project + "usdt"
        m = uni.get(old_id) or uni.get(new_id) or {}
        state = m.get("state") if m else None
        # Lifecycle events, not death booleans
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
