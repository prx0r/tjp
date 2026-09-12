"""Buy-$1000-at-listing sim. Entries wear warn-labels: FORWARD (snapshot day-0) until history lands."""
from __future__ import annotations
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade"
SIZE = 1000.0


def cohort(universe: list = None, listings: list = None) -> dict:
    uni = {m["id"]: m for m in (universe if universe is not None
                                else json.load(open(BASE / "universe.json"))["markets"])}
    ls = listings if listings is not None else json.load(open(BASE / "listings.json"))
    rows = []
    for l in ls:
        a = l["asset"].lower()
        mkts = [(i, m) for i, m in uni.items() if i.startswith(a)]
        prim = next(((i, m) for i, m in mkts if i == a + "usdt"), (mkts[0] if mkts else (None, {})))
        mid, m = prim
        rows.append({"asset": l["asset"], "announced": l["announced"],
                     "market": mid, "state": (m or {}).get("state"),
                     "market_created": ((m or {}).get("created_at") or "")[:10]})
    alive = sum(1 for r in rows if r["state"] == "enabled")
    return {"n": len(rows), "alive": alive, "dead": len(rows) - alive,
            "death_rate": round((len(rows) - alive) / max(len(rows), 1), 3), "rows": rows}
