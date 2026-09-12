"""Compute router: edge = revenue − cost − risk. Runnable form of docs/minerinfo.md."""
from __future__ import annotations
import json
from pathlib import Path


def _seed() -> dict:
    return json.loads((Path(__file__).resolve().parent.parent.parent / "docs" / "mining-seed.json").read_text())


def edges() -> list:
    s = _seed()
    out = []
    for w, rev in s["benchmarks"].items():
        if "_per_1usd" in w:
            continue
        hw = w.split("_")[0]
        cost = s["sources"].get(f"{hw}_salad")
        if cost is None:
            continue
        out.append({"workload": w, "hardware": hw, "revenue_day": rev, "cost_day": cost,
                    "edge_day": round(rev - cost, 2)})
    return sorted(out, key=lambda e: e["edge_day"], reverse=True)


def inference_edges() -> list:
    s = _seed()
    return [{"route": k, "per_1usd": v} for k, v in sorted(
        ((k, v) for k, v in s["benchmarks"].items() if "_per_1usd" in k),
        key=lambda kv: kv[1], reverse=True)]
