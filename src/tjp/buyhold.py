"""Buy-hold backtest with correct capital accounting.

Convention:
  starting_cash = size
  fee is deducted from starting_cash before buying
  No exit fee for canonical "never sell" experiment
  Returns both MTM and hypothetical liquidation values.
"""
from __future__ import annotations


def buy_hold(prices: list, entry_idx: int = 0, size: float = 1000.0,
             fee_bps: float = 20.0, slippage_bps: float = 10.0,
             charge_exit_fee: bool = False) -> dict:
    """
    prices: consecutive fills/bars.
    Buy at NEXT bar open after entry signal (anti-lookahead).
    Capital accounting: fee deducted from size BEFORE computing quantity.
    """
    if entry_idx + 1 >= len(prices):
        return {"error": "no bar after entry"}

    fill_price = prices[entry_idx + 1] * (1 + slippage_bps / 10_000)
    entry_fee = size * fee_bps / 10_000
    investable = size - entry_fee  # fee comes from starting_cash, not added on top
    qty = investable / fill_price

    equity = [round(qty * p, 2) for p in prices[entry_idx + 1:]]
    mtm_end = equity[-1] if equity else investable

    gross_mtm = mtm_end - size  # profit/loss vs original $1000
    gross_liq = mtm_end - size  # same as MTM for buy-and-hold

    exit_fee = mtm_end * fee_bps / 10_000 if charge_exit_fee else 0.0

    return {
        "fill": round(fill_price, 6),
        "qty": round(qty, 4),
        "bars": len(equity),
        "starting_cash": size,
        "entry_fee": round(entry_fee, 2),
        "investable": round(investable, 2),
        "mtm_end": round(mtm_end, 2),
        "exit_fee": round(exit_fee, 2),
        "gross_mtm": round(gross_mtm, 2),
        "net_mtm": round(mtm_end - entry_fee - size, 2),
        "gross_liq": round(mtm_end - exit_fee - size, 2),
        "net_liq": round(mtm_end - exit_fee - entry_fee - size, 2),
        "ret_mtm_pct": round((mtm_end - entry_fee - size) / size * 100, 2),
        "ret_liq_pct": round((mtm_end - exit_fee - entry_fee - size) / size * 100, 2),
        "execution_quality": "TRADE_PROXY",  # placeholder; real impl needs order book
    }
