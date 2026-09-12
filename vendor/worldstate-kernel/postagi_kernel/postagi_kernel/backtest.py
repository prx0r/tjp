"""Leakage-safe cross-sectional backtesting primitives.

Designed around the reproducibility failures highlighted by the 2026 Agentic
Trading survey: explicit as-of dates, lagged signal execution, universe handling,
transaction costs, and no same-period look-ahead.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def make_positions(scores: pd.Series, quantile: float = 0.2, gross: float = 1.0) -> pd.Series:
    if not 0 < quantile < 0.5:
        raise ValueError("quantile must be in (0,.5)")
    n=max(1,int(np.floor(len(scores)*quantile)))
    order=scores.sort_values()
    pos=pd.Series(0.0,index=scores.index)
    pos.loc[order.index[:n]]=-gross/(2*n)
    pos.loc[order.index[-n:]]=gross/(2*n)
    return pos


def walk_forward_backtest(panel: pd.DataFrame, cost_bps: float = 10.0, quantile: float = 0.2) -> tuple[pd.DataFrame,dict]:
    """Panel columns: date,ticker,score,forward_return.

    `score` must be knowable at `date`; `forward_return` is realized only after
    the trade. Each date is rebalanced independently and costs are charged on
    position turnover.
    """
    required={"date","ticker","score","forward_return"}
    if not required.issubset(panel):
        raise ValueError(f"missing {required-set(panel.columns)}")
    panel=panel.copy().sort_values(["date","ticker"])
    prev=pd.Series(dtype=float); rows=[]
    for date,g in panel.groupby("date",sort=True):
        sc=g.set_index("ticker")["score"]
        ret=g.set_index("ticker")["forward_return"]
        pos=make_positions(sc,quantile)
        idx=pos.index.union(prev.index)
        turnover=(pos.reindex(idx,fill_value=0)-prev.reindex(idx,fill_value=0)).abs().sum()
        gross=float((pos*ret.reindex(pos.index)).sum())
        cost=float(turnover*cost_bps/10000)
        net=gross-cost
        rows.append({"date":date,"gross_return":gross,"turnover":turnover,"cost":cost,"net_return":net})
        prev=pos
    out=pd.DataFrame(rows)
    r=out.net_return.to_numpy(float)
    ann_factor=12.0
    ann_return=float((np.prod(1+r)**(ann_factor/max(len(r),1)))-1) if len(r) else 0.0
    ann_vol=float(np.std(r,ddof=1)*np.sqrt(ann_factor)) if len(r)>1 else 0.0
    sharpe=ann_return/ann_vol if ann_vol>0 else 0.0
    cum=np.cumprod(1+r) if len(r) else np.array([1.0])
    peak=np.maximum.accumulate(cum)
    max_dd=float(np.min(cum/peak-1)) if len(r) else 0.0
    return out,{"annualized_return":ann_return,"annualized_vol":ann_vol,"sharpe":sharpe,"max_drawdown":max_dd,"periods":len(r),"cost_bps":cost_bps}
