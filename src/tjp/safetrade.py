"""SafeTrade discovery engine — runnable form of docs/safetradeplan.md."""
from __future__ import annotations
import json
from pathlib import Path

STAGES = ["D0_code", "D1_miners", "D2_pools", "D3_otc", "D4_creators", "D5_safetrade",
          "D6_gecko", "D7_retail_infra", "D8_second_cex", "D9_medium_cex", "D10_mainstream"]
_STORE = Path(__file__).resolve().parent.parent.parent / "docs" / "safetrade.json"


def _load() -> dict:
    return json.loads(_STORE.read_text()) if _STORE.exists() else {"projects": {}}


def _save(d: dict) -> None:
    _STORE.write_text(json.dumps(d, indent=1))


def record_stage(project: str, stage: str, date: str, evidence: str) -> dict:
    assert stage in STAGES
    from datetime import datetime, timezone

    d = _load()
    p = d["projects"].setdefault(project, {"stages": {}, "gate": {}})
    p["stages"][stage] = {"date": date, "evidence": evidence,
                           "logged": datetime.now(timezone.utc).isoformat()}
    _save(d)
    return p


GATE = ["mcap_lt_50m", "first3_cex", "working_mainnet", "open_source", "commits",
        "credible_builders", "novel_mechanism", "organic_infra", "emission_sane", "no_insider_unlock"]


def gate_check(project: str, checks: dict) -> dict:
    d = _load()
    p = d["projects"].setdefault(project, {"stages": {}, "gate": {}})
    p["gate"] = {k: bool(checks.get(k, False)) for k in GATE}
    _save(d)
    passed = all(p["gate"].values())
    return {"project": project, "buy_candidate": passed,
            "passed": sum(p["gate"].values()), "of": len(GATE)}


def discovery_multiple(peak_mcap: float, listing_mcap: float) -> float:
    return round(peak_mcap / max(listing_mcap, 1e-9), 2)


def mfe_mae(entry: float, low: float, high: float) -> dict:
    return {"mfe": round((high - entry) / entry, 2), "mae": round((low - entry) / entry, 2)}
