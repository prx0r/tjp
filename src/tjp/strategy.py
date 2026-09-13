"""Strategy engine: signals + walk-forward metrics.

Rebuilt with explicit bar semantics, proper Sharpe/Sortino, and trade ledger.
No lookahead: signal computed from bar[t-1] close, executed at bar[t] open.
"""
from __future__ import annotations
import math
import statistics
from typing import List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Bar:
    ts: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


@dataclass
class TradeRecord:
    signal_ts: str
    entry_ts: str
    entry_price: float
    entry_fee: float
    quantity: float
    exit_ts: Optional[str]
    exit_price: Optional[float]
    exit_fee: float
    gross_pnl: float
    net_pnl: float
    return_pct: float
    holding_seconds: float


def sma(values: list, n: int) -> list:
    out = []
    for i in range(len(values)):
        w = values[max(0, i - n + 1): i + 1]
        out.append(sum(w) / len(w))
    return out


def cross_signals(closes: list, fast: int = 5, slow: int = 20) -> list:
    """Signal on bar[t-1] close -> position for bar[t]."""
    f, s = sma(closes, fast), sma(closes, slow)
    sig = [0] * len(closes)
    pos = 0
    for i in range(1, len(closes)):
        if f[i - 1] <= s[i - 1] and f[i] > s[i]:
            pos = 1
        elif f[i - 1] >= s[i - 1] and f[i] < s[i]:
            pos = 0
        sig[i] = pos
    return sig


def _compute_sharpe(returns: list, bar_seconds: Optional[int] = None,
                    periods_per_year: int = 365) -> Optional[float]:
    """Annualized Sharpe. None if zero volatility (undefined)."""
    if len(returns) < 2:
        return None
    vol = statistics.pstdev(returns)
    if vol < 1e-12:
        return None
    periods = int(365.25 * 24 * 3600 / bar_seconds) if bar_seconds else periods_per_year
    return (statistics.mean(returns) / vol) * math.sqrt(periods)


def _compute_sortino(returns: list, bar_seconds: Optional[int] = None,
                     periods_per_year: int = 365, mar: float = 0.0) -> Optional[float]:
    """Annualized Sortino using downside deviation relative to MAR."""
    if len(returns) < 2:
        return None
    downside_sq = [max(0, r - mar) ** 2 for r in returns]
    dd = math.sqrt(sum(downside_sq) / len(downside_sq))
    if dd < 1e-12:
        return None
    periods = int(365.25 * 24 * 3600 / bar_seconds) if bar_seconds else periods_per_year
    return (statistics.mean(returns) - mar) / dd * math.sqrt(periods)


def _build_trades(closes: list, signals: list, bars: List[Bar], fee_bps: float) -> List[TradeRecord]:
    """Build trade ledger with proper entry/exit timestamps and fees."""
    trades = []
    entry_bar_idx = None
    for i in range(1, len(closes)):
        prev_sig = signals[i - 1]
        if prev_sig == 1 and entry_bar_idx is None:
            entry_bar_idx = i
        elif prev_sig == 0 and entry_bar_idx is not None:
            entry_bar = bars[entry_bar_idx]
            exit_bar = bars[i]
            entry_fee = entry_bar.open * fee_bps / 10_000
            exit_fee = exit_bar.open * fee_bps / 10_000
            trade_ret = (exit_bar.open / entry_bar.open) - 1
            from datetime import datetime, timezone
            t0 = datetime.fromisoformat(entry_bar.ts.replace("Z", "+00:00"))
            t1 = datetime.fromisoformat(exit_bar.ts.replace("Z", "+00:00"))
            trades.append(TradeRecord(
                signal_ts=entry_bar.ts, entry_ts=entry_bar.ts,
                entry_price=entry_bar.open, entry_fee=entry_fee, quantity=1.0,
                exit_ts=exit_bar.ts, exit_price=exit_bar.open, exit_fee=exit_fee,
                gross_pnl=trade_ret, net_pnl=trade_ret - fee_bps / 10_000 * 2,
                return_pct=round(trade_ret * 100, 4),
                holding_seconds=(t1 - t0).total_seconds(),
            ))
            entry_bar_idx = None
    return trades


def run_strategy(bars: List[Bar], signals: list, fee_bps: float = 10.0,
                 periods_per_year: int = 365) -> dict:
    """Run strategy with explicit bar timestamps and trade ledger."""
    if len(bars) < 2 or len(signals) < 1:
        return {"error": "need at least 2 bars"}

    closes = [b.close for b in bars]
    rets, pos, equity, position_log = [], 0, [1.0], [0]

    for i in range(1, len(bars)):
        target = signals[i - 1] if i - 1 < len(signals) else 0
        r = bars[i].close / bars[i - 1].close - 1
        cost = abs(target - pos) * fee_bps / 10_000 if target != pos else 0.0
        if target != pos:
            pos = target
        position_log.append(pos)
        rets.append(pos * r - cost)
        equity.append(equity[-1] * (1 + rets[-1]))

    trades = _build_trades(closes, signals, bars, fee_bps)
    total_closed = len(trades)
    wins = sum(1 for t in trades if t.net_pnl > 0)
    win_rate = wins / max(total_closed, 1)

    peak = equity[0]
    maxdd, peak_bar, trough_bar = 0.0, 0, 0
    for i, e in enumerate(equity):
        if e > peak:
            peak = e
            peak_bar = i
        dd = (peak - e) / peak if peak > 0 else 0.0
        if dd > maxdd:
            maxdd = dd
            trough_bar = i

    vol = statistics.pstdev(rets) if len(rets) > 1 else 0.0
    sharpe = _compute_sharpe(rets, periods_per_year=periods_per_year)
    sortino = _compute_sortino(rets, periods_per_year=periods_per_year)

    return {
        "total_return": round(equity[-1] - 1, 6),
        "bars": len(bars),
        "closed_trades": total_closed,
        "round_trip_win_rate": round(win_rate, 4),
        "sharpe_annualized": round(sharpe, 4) if sharpe is not None else None,
        "sortino_annualized": round(sortino, 4) if sortino is not None else None,
        "max_drawdown": round(maxdd, 6),
        "max_drawdown_peak_bar": peak_bar,
        "max_drawdown_trough_bar": trough_bar,
        "volatility_bar": round(vol, 6) if len(rets) > 1 else None,
        "equity_end": round(equity[-1], 6),
        "trades": [{"entry": t.entry_ts, "exit": t.exit_ts, "net_pnl": t.net_pnl}
                   for t in trades[:20]],
    }
