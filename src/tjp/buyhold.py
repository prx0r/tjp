"""Buy-hold backtest, BEAR rules: signal t → fill t+1 open, fees on changes only,
point-in-time universe (dead/delisted included), costs in bps.
"""
from __future__ import annotations


def buy_hold(prices: list, entry_idx: int = 0, size: float = 1000.0,
             fee_bps: float = 20.0, slippage_bps: float = 10.0) -> dict:
    """prices: consecutive fills/bars. Buy at NEXT bar open after entry signal (anti-lookahead)."""
    if entry_idx + 1 >= len(prices):
        return {"error": "no bar after entry"}
    fill = prices[entry_idx + 1] * (1 + slippage_bps / 10_000)
    qty = size / fill
    cost = size * fee_bps / 10_000
    equity = [round(qty * p, 2) for p in prices[entry_idx + 1:]]
    gross = equity[-1] - size
    exit_fee = equity[-1] * fee_bps / 10_000
    return {"fill": round(fill, 6), "qty": round(qty, 4), "bars": len(equity),
            "gross": round(gross, 2), "fees": round(cost + exit_fee, 2),
            "net": round(gross - cost - exit_fee, 2),
            "ret_pct": round((equity[-1] - exit_fee - size - cost) / size * 100, 2)}
