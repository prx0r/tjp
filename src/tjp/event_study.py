"""Event study: clock-time horizons with BTC/ETH benchmarks.

No observation-index horizons. Explicit UTC timestamps and time-based lookups.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple
from datetime import datetime, timedelta, timezone

# Clock-time horizons after entry
HORIZONS_UTC = [
    ("1h", 1 * 3600),
    ("6h", 6 * 3600),
    ("24h", 24 * 3600),
    ("3d", 3 * 24 * 3600),
    ("7d", 7 * 24 * 3600),
    ("14d", 14 * 24 * 3600),
    ("30d", 30 * 24 * 3600),
    ("90d", 90 * 24 * 3600),
    ("180d", 180 * 24 * 3600),
    ("365d", 365 * 24 * 3600),
]


@dataclass
class TimestampedPrice:
    ts: datetime  # UTC
    price: float


def price_at_horizon(
    entry: TimestampedPrice,
    prices: List[TimestampedPrice],
    horizon_seconds: int,
) -> Optional[float]:
    """Find first price at or after entry + horizon. Returns None if not found."""
    target = entry.ts + timedelta(seconds=horizon_seconds)
    for p in sorted(prices, key=lambda x: x.ts):
        if p.ts >= target:
            return p.price
    return None


def event_study_entry(
    listing_ts: datetime,
    asset_prices: List[TimestampedPrice],
    btc_prices: List[TimestampedPrice],
    eth_prices: List[TimestampedPrice],
) -> dict:
    """Compute forward returns at clock horizons + benchmarks for one listing event."""
    entry_price = None
    for p in sorted(asset_prices, key=lambda x: x.ts):
        if p.ts >= listing_ts:
            entry_price = p.price
            break
    if entry_price is None:
        return {"error": "no price found after listing"}

    entry = TimestampedPrice(ts=listing_ts, price=entry_price)
    results = {
        "entry_price": entry_price,
        "entry_ts": listing_ts.isoformat(),
        "returns": {},
        "benchmark_returns": {},
    }

    for name, secs in HORIZONS_UTC:
        target_price = price_at_horizon(entry, asset_prices, secs)
        btc_price = price_at_horizon(entry, btc_prices, secs)
        eth_price = price_at_horizon(entry, eth_prices, secs)

        if target_price is not None:
            results["returns"][name] = round((target_price - entry_price) / entry_price, 6)
        if btc_price is not None:
            entry_btc = price_at_horizon(TimestampedPrice(ts=listing_ts, price=1.0), btc_prices, 0) or 1.0
            # For benchmark, we need the actual BTC price at listing time
            btc_entry = None
            for p in sorted(btc_prices, key=lambda x: x.ts):
                if p.ts >= listing_ts:
                    btc_entry = p.price
                    break
            if btc_entry and btc_price:
                results["benchmark_returns"][f"btc_{name}"] = round((btc_price - btc_entry) / btc_entry, 6)
        if eth_price is not None:
            eth_entry = None
            for p in sorted(eth_prices, key=lambda x: x.ts):
                if p.ts >= listing_ts:
                    eth_entry = p.price
                    break
            if eth_entry and eth_price:
                results["benchmark_returns"][f"eth_{name}"] = round((eth_price - eth_entry) / eth_entry, 6)

    # MFE/MAE per horizon
    results["mfe_mae"] = {}
    for name, secs in HORIZONS_UTC:
        window_end = listing_ts + timedelta(seconds=secs)
        prices_in_window = [p for p in asset_prices if listing_ts <= p.ts <= window_end]
        if prices_in_window:
            max_p = max(p.price for p in prices_in_window)
            min_p = min(p.price for p in prices_in_window)
            results["mfe_mae"][name] = {
                "mfe_pct": round((max_p - entry_price) / entry_price, 6),
                "mae_pct": round((entry_price - min_p) / entry_price, 6),
            }

    return results
