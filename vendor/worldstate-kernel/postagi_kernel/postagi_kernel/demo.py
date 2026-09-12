from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd
from .io import load_scenarios, load_companies
from .scoring import rank_companies
from .backtest import walk_forward_backtest

ROOT=Path(__file__).resolve().parents[1]

def run_demo(root: Path=ROOT):
    scenarios=load_scenarios(root/"configs"/"default.yaml")
    companies=load_companies(root/"data"/"demo_companies.csv")
    aux=pd.read_csv(root/"data"/"demo_aux_scores.csv").set_index("ticker").to_dict("index")
    ranking=rank_companies(companies,scenarios,aux)
    ranking.to_csv(root/"reports"/"demo_company_scores.csv",index=False)
    panel=pd.read_csv(root/"data"/"demo_backtest_panel.csv")
    bt,metrics=walk_forward_backtest(panel,cost_bps=10,quantile=.2)
    bt.to_csv(root/"reports"/"demo_backtest_returns.csv",index=False)
    (root/"reports"/"demo_backtest_metrics.json").write_text(json.dumps(metrics,indent=2))
    return ranking,metrics
