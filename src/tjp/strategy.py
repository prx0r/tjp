"""Strategy engine: signals + walk-forward metrics. BEAR rules (t+1 fill, costs on change)."""
from __future__ import annotations
import statistics


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


def run_strategy(prices: list, signals: list, fee_bps: float = 10.0) -> dict:
    """signals[i] = position for bar i+1 (anti-lookahead built in). Returns ML-type report."""
    rets, pos, equity, trades, wins = [], 0, [1.0], 0, 0
    entry = 0.0
    for i in range(1, len(prices)):
        target = signals[i - 1] if i - 1 < len(signals) else 0
        r = prices[i] / prices[i - 1] - 1
        if target != pos:
            cost = abs(target - pos) * fee_bps / 10_000
            trades += 1
            if pos == 1 and r > 0:
                wins += 1
            if target == 1:
                entry = i
            pos = target
        else:
            cost = 0.0
        rets.append(pos * r - cost)
        equity.append(equity[-1] * (1 + rets[-1]))
    tot = equity[-1] - 1
    peak, maxdd = equity[0], 0.0
    for e in equity:
        peak = max(peak, e)
        maxdd = max(maxdd, (peak - e) / peak)
    vol = statistics.pstdev(rets) if len(rets) > 1 else 0.0
    return {"total_ret": round(tot, 4), "bars": len(prices), "trades": trades,
            "win_rate": round(wins / max(trades, 1), 3),
            "sharpe_like": round((statistics.mean(rets) / vol) if vol else 0.0, 3),
            "max_drawdown": round(maxdd, 4), "equity_end": round(equity[-1], 4)}
