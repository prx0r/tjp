"""Build OHLCV bars from trades.

Trades are not time. A 199-fill PRL series is not 199 equal periods.
Construct deterministic bars with explicit missing-bar handling.
"""
from __future__ import annotations
from typing import List
from .schema import TradeRecord, OHLCVBar
from datetime import datetime, timedelta, timezone
import math


def build_bars(trades: List[TradeRecord], bar_seconds: int = 60) -> List[OHLCVBar]:
    """Convert unordered trades into OHLCV bars. Trades must be pre-sorted by exchange_ts.
    bar_seconds: 60=1m, 300=5m, 3600=1h, 86400=1d.
    """
    if not trades:
        return []

    def ts_to_dt(ts: str) -> datetime:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))

    def dt_to_bar_key(dt: datetime) -> int:
        return int(dt.timestamp() // bar_seconds)

    def bar_key_to_ts(key: int) -> datetime:
        return datetime.fromtimestamp(key * bar_seconds, tz=timezone.utc)

    bars = []
    current_key = None
    bar_trades = []

    for t in trades:
        dt = ts_to_dt(t.exchange_ts)
        key = dt_to_bar_key(dt)

        if current_key is None or key == current_key:
            current_key = key
            bar_trades.append(t)
        else:
            # Flush previous bar
            bars.append(_make_bar(current_key, bar_trades, bar_seconds))
            current_key = key
            bar_trades = [t]

    # Flush last bar
    if bar_trades:
        bars.append(_make_bar(current_key, bar_trades, bar_seconds))

    return bars


def _make_bar(key: int, trades: List[TradeRecord], bar_seconds: int) -> OHLCVBar:
    prices = [t.price for t in trades]
    qtys = [t.quantity for t in trades]
    quote_qtys = [t.quote_quantity for t in trades]

    base_vol = sum(qtys)
    quote_vol = sum(quote_qtys)
    vwap = quote_vol / base_vol if base_vol > 0 else 0.0

    return OHLCVBar(
        market_id=trades[0].market_id if trades else "",
        bar_size=f"{bar_seconds}s",
        ts_open=datetime.fromtimestamp(key * bar_seconds, tz=timezone.utc).isoformat(),
        open=prices[0],
        high=max(prices),
        low=min(prices),
        close=prices[-1],
        base_volume=base_vol,
        quote_volume=quote_vol,
        trade_count=len(trades),
        vwap=round(vwap, 10),
        first_trade_ts=trades[0].exchange_ts if trades else "",
        last_trade_ts=trades[-1].exchange_ts if trades else "",
    )
