import pandas as pd
from postagi_kernel.backtest import walk_forward_backtest

def test_backtest_costs_and_periods():
    rows=[]
    for d in ["2025-01-31","2025-02-28"]:
      for i in range(10):
        rows.append({"date":d,"ticker":f"T{i}","score":i,"forward_return":i/100})
    out,m=walk_forward_backtest(pd.DataFrame(rows),cost_bps=10,quantile=.2)
    assert len(out)==2 and m["periods"]==2
    assert (out.cost>=0).all()
