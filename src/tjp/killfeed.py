"""KillFeed: five binaries per trade. Runnable form of docs/killfeedtop.md."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

WEIGHTS = {"NEED": 35, "GAP": 25, "LAG": 20, "WTP": 12, "SUB": 8}
STATES = ("TRUE", "WATCH", "FALSE")
_STORE = Path(__file__).resolve().parent.parent.parent / "docs" / "killfeed.json"


def _load() -> dict:
    return json.loads(_STORE.read_text()) if _STORE.exists() else {}


def _save(d: dict) -> None:
    _STORE.write_text(json.dumps(d, indent=1))


def k_score(states: dict) -> float:
    v = {"TRUE": 1.0, "WATCH": 0.5, "FALSE": 0.0}
    return round(sum(v[states.get(k, "TRUE")] * w for k, w in WEIGHTS.items()), 1)


def verdict(trade_id: str) -> dict:
    d = _load().get(trade_id, {})
    states = d.get("states", {})
    k = k_score(states)
    if states.get("NEED") == "FALSE" or states.get("GAP") == "FALSE":
        band = "KILL"
    elif states.get("LAG") == "FALSE":
        band = "LATE — DO NOT ADD"
    elif k >= 85:
        band = "SCARCITY RENT ACTIVE"
    elif k >= 60:
        band = "WATCH"
    else:
        band = "KILL"
    return {"trade_id": trade_id, "k": k, "band": band, "states": states}


def set_state(trade_id: str, cond: str, state: str, evidence: str) -> dict:
    assert cond in WEIGHTS and state in STATES
    d = _load()
    t = d.setdefault(trade_id, {"states": {}, "log": []})
    t["states"][cond] = state
    t["log"].append({"cond": cond, "state": state, "evidence": evidence,
                     "ts": datetime.now(timezone.utc).isoformat()})
    _save(d)
    return verdict(trade_id)
