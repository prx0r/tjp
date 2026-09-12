"""Candidate funnel: DISCOVER → FUNDAMENTAL → UNDERVALUED → CATALYST → REFLEXIVITY → GOLD → TRADE → FALSIFY/EXIT."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

STAGES = ["DISCOVER", "FUNDAMENTAL", "UNDERVALUED", "CATALYST", "REFLEXIVITY", "GOLD", "TRADE", "FALSIFY/EXIT"]
_STORE = Path(__file__).resolve().parent.parent.parent / "docs" / "funnel.json"


def _load() -> dict:
    if _STORE.exists():
        return json.loads(_STORE.read_text())
    return {}


def _save(d: dict) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    _STORE.write_text(json.dumps(d, indent=1))


def stage_of(trade_id: str) -> str:
    return _load().get(trade_id, {}).get("stage", "DISCOVER")


def advance(trade_id: str, to: str, note: str = "") -> dict:
    if to not in STAGES:
        return {"error": f"unknown stage {to}"}
    d = _load()
    cur = d.get(trade_id, {"stage": "DISCOVER", "history": []})
    if STAGES.index(to) < STAGES.index(cur["stage"]) and to != "FALSIFY/EXIT":
        return {"error": f"cannot move back from {cur['stage']} to {to}"}
    cur["history"].append({"from": cur["stage"], "to": to, "note": note, "ts": datetime.now(timezone.utc).isoformat()})
    cur["stage"] = to
    d[trade_id] = cur
    _save(d)
    return cur
