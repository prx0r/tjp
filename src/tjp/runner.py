"""Event-study runner: T0-anchored returns + MFE/MAE + cohort report + gate F."""
from __future__ import annotations
import json
from pathlib import Path

from .backtest import event_returns, mfe_mae, discovery_multiple, cohort_stats, gate_f

BASE = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade"


def run() -> dict:
    listings = json.loads((BASE / "listings.json").read_text())
    res = {"listings": [], "multiples": [], "gates": []}
    for l in listings:
        res["listings"].append({"asset": l["asset"], "announced": l["announced"], "t0_note": l.get("t0_note")})
        g = gate_f({k: False for k in
                    ["mcap_lt_50m", "first3_cex", "working_mainnet", "open_source", "commits",
                     "credible_builders", "novel_mechanism", "organic_infra", "emission_sane", "no_insider_unlock"]})
        res["gates"].append({"asset": l["asset"], **g, "note": "evidence TBD per listing"})
    res["cohort"] = cohort_stats(res["multiples"])
    res["note"] = "multiples empty until mcap-at-T0 + peak captured per listing"
    (BASE / "report.json").write_text(json.dumps(res, indent=1))
    return res
