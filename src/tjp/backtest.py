"""SafeTrade backtest engine — runnable form of docs/safetradeplan.md.

Rules: first executable ask (never close), MFE+MAE alongside terminal, matched benchmarks,
complete universe incl. dead/delisted, world frozen at T0.
"""
from __future__ import annotations
import statistics


def event_returns(entry: float, closes: list) -> dict:
    return {f"t{i}": round((c - entry) / entry, 4) for i, c in enumerate(closes)}


def mfe_mae(entry: float, series: list) -> dict:
    return {"mfe": round((max(series) - entry) / entry, 4),
            "mae": round((min(series) - entry) / entry, 4)}


def discovery_multiple(peak_mcap: float, listing_mcap: float) -> float:
    return round(peak_mcap / max(listing_mcap, 1e-9), 2)


def cohort_stats(multiples: list) -> dict:
    ms = sorted(multiples)
    n = len(ms)
    pct = lambda x: round(sum(1 for m in ms if m >= x) / n, 3) if n else 0.0
    return {"n": n, "median": round(statistics.median(ms), 2) if n else 0.0,
            "p2x": pct(2), "p5x": pct(5), "p10x": pct(10), "p50x": pct(50),
            "zeroed": round(sum(1 for m in ms if m <= 0.05) / n, 3) if n else 0.0}


def gate_f(candidate: dict) -> dict:
    keys = ["mcap_lt_50m", "first3_cex", "working_mainnet", "open_source", "commits",
            "credible_builders", "novel_mechanism", "organic_infra", "emission_sane", "no_insider_unlock"]
    got = {k: bool(candidate.get(k, False)) for k in keys}
    return {"buy_candidate": all(got.values()), "passed": sum(got.values()), "of": len(keys)}
