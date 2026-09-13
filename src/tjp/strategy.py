"""Strategy engine: signals + walk-forward metrics.

Rebuilt: correct Sharpe (annualized), correct win rate (round trips only),
proper trade accounting.
"""
from __future__ import annotations
import math
import statistics
from typing import Optional


def sma(values: list, n: int) -> list:
    out = []
    for i in range(len(values)):
        w = values[max(0, i - n + 1): i + 1]
        out.append(sum(w) / len(w))
    return out


def cross_signals(prices: list, fast: int = 5, slow: int = 20) -> list:
    f, s = sma(prices, fast), sma(prices, slow)
    sig, pos = [], 0
    for i in range(1, len(prices)):
        if f[i - 1] <= s[i - 1] and f[i] > s[i]:
            pos = 1
        elif f[i - 1] >= s[i - 1] and f[i] < s[i]:
            pos = 0
        sig.append(pos)
    return sig


def _compute_sharpe(returns: list, periods_per_year: int = 365) -> float:
    """Annualized Sharpe ratio assuming risk-free rate = 0."""
    if len(returns) < 2:
        return 0.0
    mean_r = statistics.mean(returns)
    vol = statistics.pstdev(returns)
    if vol == 0:
        return 0.0
    return (mean_r / vol) * math.sqrt(periods_per_year)


def _compute_sortino(returns: list, periods_per_year: int = 365) -> float:
    """Annualized Sortino ratio."""
    if len(returns) < 2:
        return 0.0
    mean_r = statistics.mean(returns)
    downside = [r for r in returns if r < 0]
    if not downside:
        return float('inf') if mean_r > 0 else 0.0
    downside_vol = statistics.pstdev(downside)
    if downside_vol == 0:
        return 0.0
    return (mean_r / downside_vol) * math.sqrt(periods_per_year)


def _count_round_trip_wins(positions: list, returns: list) -> tuple:
    """Count completed round trips and wins from position changes.
    A round trip completes when position goes 1→0.
    positions: length = len(prices); returns: length = len(prices)-1 (returns[j] = bar j+1 return).
    """
    trades = []
    entry_bar = None
    for i in range(1, len(positions)):
        prev, curr = positions[i - 1], positions[i]
        if prev == 0 and curr == 1:
            entry_bar = i
        elif prev == 1 and curr == 0 and entry_bar is not None:
            trade_ret = 1.0
            for j in range(entry_bar, i):
                trade_ret *= (1 + returns[j])
            trade_ret -= 1
            trades.append({"entry": entry_bar, "exit": i, "return": trade_ret})
            entry_bar = None
    wins = sum(1 for t in trades if t["return"] > 0)
    return trades, wins


def run_strategy(prices: list, signals: list, fee_bps: float = 10.0,
                 periods_per_year: int = 365) -> dict:
    """signals[i] = position for bar i+1 (anti-lookahead built in)."""
    if len(prices) < 2:
        return {"error": "need at least 2 prices"}

    rets = []
    pos = 0
    equity = [1.0]
    position_log = [0]

    for i in range(1, len(prices)):
        target = signals[i - 1] if i - 1 < len(signals) else 0
        r = prices[i] / prices[i - 1] - 1
        cost = 0.0
        if target != pos:
            cost = abs(target - pos) * fee_bps / 10_000
            pos = target
        position_log.append(pos)
        rets.append(pos * r - cost)
        equity.append(equity[-1] * (1 + rets[-1]))

    trades, wins = _count_round_trip_wins(position_log, rets)
    total_closed = len(trades)
    win_rate = wins / max(total_closed, 1)

    # Peak / max drawdown
    peak = equity[0]
    maxdd = 0.0
    peak_bar = 0
    for i, e in enumerate(equity):
        if e > peak:
            peak = e
            peak_bar = i
        dd = (peak - e) / peak if peak > 0 else 0.0
        if dd > maxdd:
            maxdd = dd

    vol = statistics.pstdev(rets) if len(rets) > 1 else 0.0
    sharpe = _compute_sharpe(rets, periods_per_year)
    sortino = _compute_sortino(rets, periods_per_year)

    total_ret = equity[-1] - 1

    return {
        "total_return": round(total_ret, 6),
        "bars": len(prices),
        "closed_trades": total_closed,
        "round_trip_win_rate": round(win_rate, 4),
        "sharpe_annualized": round(sharpe, 4),
        "sortino_annualized": round(sortino, 4),
        "max_drawdown": round(maxdd, 6),
        "max_drawdown_bar": peak_bar,
        "volatility_bar": round(vol, 6) if len(rets) > 1 else None,
        "equity_end": round(equity[-1], 6),
        "trades": trades[:20],  # cap output for readability
    }
