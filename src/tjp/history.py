"""Price-history builder: tape JSONL + snapshots → continuous per-market series."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade"


def tape_series(market: str) -> list:
    f = BASE / "tape" / f"{market}.jsonl"
    if not f.exists():
        return []
    rows = [json.loads(line) for line in f.read_text().splitlines() if line.strip()]
    rows.sort(key=lambda r: r.get("created_at", ""))
    return [(r.get("created_at"), float(r["price"])) for r in rows if float(r.get("price", 0)) > 0]


def snapshot_series(pair: str) -> list:
    out = []
    for f in sorted((BASE / "snapshots").glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        ts = d.get("ts")
        for r in d.get("rows", []):
            if r.get("pair") == pair and r.get("last"):
                out.append((ts, float(r["last"])))
    return sorted(out)
