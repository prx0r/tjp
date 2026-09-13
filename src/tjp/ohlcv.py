"""Build OHLCV bars from trades.

Requires pre-sorted trades. Fails on unsorted input (no silent repair).
Explicit missing-bar tracking for research horizons.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from .schema import TradeRecord, OHLCVBar
from datetime import datetime, timezone


@dataclass
class BarWithMissingness:
    bar: OHLCVBar
    is_missing: bool
    target_ts: Optional[str] = None
    actual_mark_ts: Optional[str] = None
    mark_delay_seconds: Optional[float] = None


def build_bars(trades: List[TradeRecord], bar_seconds: int = 60) -> List[BarWithMissingness]:
    """Build bars from pre-sorted trades. Raises ValueError on unsorted input.
    Inserts MISSING bars for gaps in the sequence.
    """
    if not trades:
        return []

    def ts_to_dt(ts: str) -> datetime:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))

    def dt_to_bar_key(dt: datetime) -> int:
        return int(dt.timestamp() // bar_seconds)

    def bar_key_to_ts(key: int) -> str:
        return datetime.fromtimestamp(key * bar_seconds, tz=timezone.utc).isoformat()

    # Verify monotonicity
    keys = [dt_to_bar_key(ts_to_dt(t.exchange_ts)) for t in trades]
    for i in range(1, len(keys)):
        if keys[i] < keys[i - 1]:
            raise ValueError(
                f"Unsorted trades: bar {keys[i]} at index {i} precedes bar {keys[i-1]} at {i-1}. "
                "Sort trades by exchange_ts before building bars."
            )

    bars = []
    current_key = None
    bar_trades = []
    prev_key = None

    for t in trades:
        dt = ts_to_dt(t.exchange_ts)
        key = dt_to_bar_key(dt)

        # Insert missing bars
        if prev_key is not None and key > prev_key + 1:
            for mk in range(prev_key + 1, key):
                bars.append(BarWithMissingness(
                    bar=OHLCVBar(
                        market_id=trades[0].market_id,
                        bar_size=f"{bar_seconds}s",
                        ts_open=bar_key_to_ts(mk),
                        open=0.0, high=0.0, low=0.0, close=0.0,
                        base_volume=0.0, quote_volume=0.0, trade_count=0, vwap=0.0,
                    ),
                    is_missing=True,
                    target_ts=bar_key_to_ts(mk),
                ))

        if current_key is None or key == current_key:
            current_key = key
            bar_trades.append(t)
        else:
            bars.append(_make_bar(current_key, bar_trades, bar_seconds))
            current_key = key
            bar_trades = [t]

        prev_key = key

    if bar_trades:
        bars.append(_make_bar(current_key, bar_trades, bar_seconds))

    return bars


def _make_bar(key: int, trades: List[TradeRecord], bar_seconds: int) -> BarWithMissingness:
    prices = [t.price for t in trades]
    qtys = [t.quantity for t in trades]
    quote_qtys = [t.quote_quantity for t in trades]
    base_vol = sum(qtys)
    quote_vol = sum(quote_qtys)
    vwap = quote_vol / base_vol if base_vol > 0 else 0.0

    bar = OHLCVBar(
        market_id=trades[0].market_id,
        bar_size=f"{bar_seconds}s",
        ts_open=datetime.fromtimestamp(key * bar_seconds, tz=timezone.utc).isoformat(),
        open=prices[0], high=max(prices), low=min(prices), close=prices[-1],
        base_volume=base_vol, quote_volume=quote_vol, trade_count=len(trades),
        vwap=round(vwap, 10),
        first_trade_ts=trades[0].exchange_ts,
        last_trade_ts=trades[-1].exchange_ts,
    )
    return BarWithMissingness(
        bar=bar, is_missing=False,
        target_ts=bar.ts_open,
        actual_mark_ts=bar.last_trade_ts,
        mark_delay_seconds=(datetime.fromisoformat(bar.last_trade_ts.replace("Z", "+00:00"))
                           - datetime.fromisoformat(bar.ts_open.replace("Z", "+00:00"))).total_seconds(),
    )
